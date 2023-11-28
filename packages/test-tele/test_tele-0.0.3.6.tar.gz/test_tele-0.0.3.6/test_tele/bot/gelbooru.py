import logging
from typing import List, Optional


import json
import requests
import urllib.parse

from bs4 import BeautifulSoup
from os.path import splitext, basename

from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
                            InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation)


API_KEY = "c599ca62bbfc294b76492900d5d3066fc42fde83704e4c00bb8b5719b5753c76"
USER_ID = "1271918"


async def get_images(query: str, pid: int = 0, api_key: str = None, user_id: str = None) -> List[dict]:
    tags = urllib.parse.quote(query.strip())
    request_url = f'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=50&pid={pid}&tags={tags}'
    if api_key and user_id:
        request_url += f'&api_key={api_key}&user_id={user_id}'

    response = requests.get(request_url)
    if response.status_code != 200:
        raise ConnectionError(f'Non-200 response from Gelbooru, got {response.status_code} instead')

    try:
        json_response = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        return []

    results = []
    if 'post' not in json_response:
        return results
    elif isinstance(json_response['post'], dict):
        json_response_images_data = [json_response['post']]
    else:
        json_response_images_data = json_response['post']

    for json_item in json_response_images_data:
        full_url = json_item['file_url'].replace('img3.', 'img1.')   # img3 seems to be faulty at the moment
        has_sample = json_item.get('sample') and json_item['sample'] != '0'
        is_video = full_url.endswith('.mp4') or full_url.endswith('.webm')
        if has_sample and not is_video:
            full_url = await get_sample_url(json_item['file_url'])
            height = json_item['sample_height']
            width = json_item['sample_width']
        else:
            height = json_item['height']
            width = json_item['width']

        extension = splitext(basename(full_url))[1]
        if extension not in ['.jpeg', '.jpg', '.gif', '.png', '.webm', '.mp4']:
            continue

        result = dict()
        result['id'] = json_item['id']
        result['page_url'] = await get_page_url_from_image_id(json_item['id'])
        result['rating'] = json_item['rating']
        result['thumbnail_url'] = await get_thumbnail_url(json_item['file_url'])
        result['full_url'] = full_url
        result['image_height'] = height
        result['image_width'] = width
        results.append(result)
    return results


async def get_thumbnail_url(full_url: str) -> str:
    prefix1, prefix2, image_name = full_url.split('/')[-3:]
    image_name = image_name.split('.')[0]
    return f'https://gelbooru.com/thumbnails/{prefix1}/{prefix2}/thumbnail_{image_name}.jpg'


async def get_sample_url(full_url: str) -> str:
    prefix1, prefix2, image_name = full_url.split('/')[-3:]
    image_name = image_name.split('.')[0]
    return f'https://img1.gelbooru.com//samples/{prefix1}/{prefix2}/sample_{image_name}.jpg'


async def get_page_url_from_image_id(image_id: int) -> str:
    return f'https://gelbooru.com/index.php?page=post&s=view&id={str(image_id)}'


async def autocomplete(query: str) -> Optional[str]:
    """ Autocomplete last word in query to the most popular Gelbooru tag that starts with this word.
        Do nothing if the word is already a valid Gelbooru tag. """
    split_query = query.rsplit(' ', 1)
    last_tag = split_query[-1]
    rest_of_query = split_query[0] if len(split_query) > 1 else ''

    if not last_tag or last_tag.startswith(('-', '*', '~')) or last_tag.endswith('~') or ':' in last_tag:
        return query

    encoded_last_tag = urllib.parse.quote(last_tag)
    request_url = f'https://gelbooru.com/index.php?page=autocomplete2&term={encoded_last_tag}&limit=10'
    response = requests.get(request_url)
    if response.status_code != 200:
        raise ConnectionError(f'Non-200 response from Gelbooru, got {response.status_code} instead')

    try:
        autocompleted_tag_list = list(tag['value'] for tag in json.loads(response.text))
        # Do not autocomplete last word if it is already a valid tag
        if last_tag in autocompleted_tag_list:
            autocompleted_tag = last_tag
        else:
            autocompleted_tag = autocompleted_tag_list[0]
    except (IndexError, KeyError, json.decoder.JSONDecodeError):
        return None

    if rest_of_query:
        return f'{rest_of_query} {autocompleted_tag}'
    else:
        return autocompleted_tag


async def image_keyboard(image: dict, query: str) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton("💾" ,
                                     callback_data=str(image['id'])),
                InlineKeyboardButton("🔗",
                                     url=f'https://gelbooru.com/index.php?page=post&s=view&id={image["id"]}'),
                InlineKeyboardButton("🔄",
                                     switch_inline_query_current_chat=query),
                ]]
    return InlineKeyboardMarkup(buttons)


connection_error_message = InputTextMessageContent(message_text='Network error.')
connection_error_response = InlineQueryResultArticle(
    id='networkerror', title='No response from Gelbooru',
    description='Please try again a little later.',
    input_message_content=connection_error_message)


async def get_file(url_page):
    request_url = url_page
    response = requests.get(request_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    og_image = soup.find('meta', attrs={'property': 'og:image'})
    if og_image:
        og_image_url = og_image.get('content')
        try:
            url = og_image_url.replace('img3.', 'img1.')
        except:
            url = og_image_url.replace('.webm', '.mp4')
        return url
    return


async def inline_gelbooru(client, inline_query):
    """Handle inline query for gelbooru search"""
    query = inline_query.query

    if not query:
        return

    offset = inline_query.offset
    pid = int(offset) if offset else 0

    query = await autocomplete(query)
    if query is None:
        err_result = [
            InlineQueryResultArticle(
                'Could not autocomplete last tag', InputTextMessageContent(message_text='Could not find provided tags.'), id='notags', 
                description='Gelbooru tag list does not contain any match.\nPlease fix a typo or try a different tag.')
        ]
        await client.answer_inline_query(
            inline_query.id,
            results=err_result
        )
        return
    
    results = []
    images = await get_images(query, pid=pid, api_key=API_KEY, user_id=USER_ID)
    if pid == 0 and not images:
        err_result = [
            InlineQueryResultArticle(
                'No results found', InputTextMessageContent(message_text='No results found with those tags.'), 
                id='noresults', description='Please try different tags.')
        ]
        await client.answer_inline_query(
            inline_query.id,
            results=err_result
        )
        return

    for image in images:
        try:
            if image['full_url'].endswith('.webm') or image['full_url'].endswith('.mp4'):
                result = InlineQueryResultVideo(
                    video_url=image['full_url'],
                    thumb_url=image['thumbnail_url'],
                    title=f'Video {image["image_width"]}×{image["image_height"]}',
                    id=str(image['id']),
                    mime_type='video/mp4',
                    reply_markup=await image_keyboard(image=image, query=query),
                )
            elif image['full_url'].endswith('.gif'):
                result = InlineQueryResultAnimation(
                    animation_url=image['full_url'],
                    animation_width=image['image_width'],
                    animation_height=image['image_height'],
                    thumb_url=image['thumbnail_url'],
                    id=str(image['id']),
                    title=str(image['id']),
                    reply_markup=await image_keyboard(image=image, query=query),
                )
            else:
                result = InlineQueryResultPhoto(
                    photo_url=image['full_url'],
                    thumb_url=image['thumbnail_url'],
                    photo_width=image['image_width'],
                    photo_height=image['image_height'],
                    id=str(image['id']),
                    title=str(image['id']),
                    reply_markup=await image_keyboard(image=image, query=query),
                )
            results.append(result)
        except Exception as e:
            logging.error(e)
            pass
    
    try:
        await client.answer_inline_query(
            inline_query.id,
            results=results,
            is_gallery=True,
            next_offset=str(pid + 1)
        )
    except Exception as err:
        logging.error(err)


async def callback(client, callback_query):
    """Handle callback query from inline keyboard"""
    data = callback_query.data
    if data:
        data = f'https://gelbooru.com/index.php?page=post&s=view&id={data}'
        image_file = await get_file(data)
        if image_file:
            return image_file
        
    await callback_query.answer()




