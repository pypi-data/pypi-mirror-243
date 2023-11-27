import re
from datetime import datetime, timedelta

#bracketed_data_pattern = r'(\w+)\((\d+)\)'
bracketed_data_pattern = r'^(.*?)\((\d+)\)$'



number_pattern = r'(\d+)'

business_hour_range_pattern = r'(\w+):\s+(\d{2}:\d{2}) - (\d{2}:\d{2})'
day_pattern = r'(\d+\.\d+) \((\w+)\)'
blog_id_pattern = r'\?bid=([a-fA-F0-9]+)'
days_ago_pattern = r'(\d+)일전'
width_percentage_pattern = r'width:(\d+)%;'
background_image_url_pattern = r"url\(['\"](https?://[^)]+)['\"]\)"

special_business_hour_range_pattern = r'^(.*?): (\d{2}:\d{2}) - (\d{2}:\d{2})$'
special_business_hour_parsing_range_pattern = r'^(.*?): (\d{2}:\d{2}) - (\d{2}:\d{2})$'

special_business_hour_single_pattern = r'^(.*?): (\d{2}:\d{2})$'
special_business_hour_parsing_single_pattern = r'^(.*?): (\d{2}:\d{2})$'

special_day_without_time_pattern = r'^[^0-9:-]+$'

def is_special_day_without_time_pattern(text):
    match = get_match_for_pattern(text, special_day_without_time_pattern)
    if match:
        return True
    else:
        return False

def parse_special_day_without_time_pattern(text):
    match = get_match_for_pattern(text, special_day_without_time_pattern)

    return match

def is_single_special_business_hour(text):
    # 정규표현식으로 패턴 확인
    if re.search(special_business_hour_single_pattern, text):
        return True
    else:
        return False


def parse_single_special_business_hour(text):
    # 정규표현식으로 패턴 확인
    match = get_match_for_pattern(text, special_business_hour_parsing_single_pattern)
    if not match:
        return None
    return {
        "type":match.group(1),
        "time": match.group(2)
    }

def parse_special_business_hour(text):
    match = re.search(special_business_hour_parsing_range_pattern, text)
    if match:
        type = match.group(1)
        start_time = match.group(2)
        end_time = match.group(2)
        return {"type": type, "start_time": start_time, "end_time":end_time}
    else:
        return None  # 매칭되는 패턴이 없을 경우 None 반환


def is_special_business_hour(text):
    # 정규표현식으로 패턴 확인
    if re.search(special_business_hour_range_pattern, text):
        return True
    else:
        return False


def has_image_tag(tag_soup):
    img_tag = tag_soup.find("img")
    if img_tag:
        return True
    else:
        return False


def calculate_date_from_days_ago(days_ago, base_date=None):
    # N일전의 날짜 계산
    calculated_date = base_date - timedelta(days=days_ago)
    # 월과 일 형식으로 포맷
    formatted_date = calculated_date.strftime('%m월 %d일')
    return formatted_date


def parse_width_value_in_style(text):
    match = re.search(width_percentage_pattern, text)
    if match:
        return int(match.group(1))
    else:
        return None  # 매칭되는 패턴이 없을 경우 None 반환


def convert_css_width_percentage_to_star_point(text):
    percentage = parse_width_value_in_style(text)
    if not percentage:
        return 0
    if percentage == 0:
        return 0
    elif percentage == 20:
        return 1
    elif percentage == 40:
        return 2
    elif percentage == 60:
        return 3
    elif percentage == 80:
        return 4
    elif percentage == 100:
        return 5


def parse_background_image_url_in_style(text):
    match = re.search(background_image_url_pattern, text)
    if match:
        return match.group(1)
    else:
        return None  # 매칭되는 패턴이 없을 경우 None 반환


def parse_days_ago(text):
    match = re.search(days_ago_pattern, text)
    if match:
        days_ago = int(match.group(1))
        return days_ago
    else:
        return None  # 매칭되는 패턴이 없을 경우 None 반환


def is_days_ago(text):
    # 정규표현식으로 패턴 확인
    if re.search(days_ago_pattern, text):
        return True
    else:
        return False


def get_match_for_pattern(text, pattern):
    matches = re.search(pattern, text)
    return matches


def parse_blog_id_from_query_parameter(text):
    match = get_match_for_pattern(text, blog_id_pattern)
    id = match.group(1)
    return id


def parse_number(text: str):
    match = get_match_for_pattern(text, number_pattern)
    number = match.group(1)
    return number


def parse_business_hour_pattern(text):
    match = get_match_for_pattern(text, business_hour_range_pattern)
    type = match.group(1)
    start_time = match.group(2)
    end_time = match.group(3)
    return {
        "type": type,
        "start_time": start_time,
        "end_time": end_time,
    }


def is_date_and_day_of_the_week_pattern(text):
    match = get_match_for_pattern(text, day_pattern)
    if match:
        return True
    else:
        return False

def parse_date_and_day_of_the_week_pattern(text):
    match = get_match_for_pattern(text, day_pattern)
    date = match.group(1)
    day_of_week = match.group(2)
    return {
        "date": date,
        "day_of_week": day_of_week
    }


def parse_bracketed_data(text):
    match = get_match_for_pattern(text, bracketed_data_pattern)

    name = match.group(1)
    value = match.group(2)
    return {
        "name": name,
        "value": value
    }
