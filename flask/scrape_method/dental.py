import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os, csv, sys, math, pytz
from datetime import datetime

headers_pc = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.2.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36", }

# ! supeの作成
def create_supe(url: str) -> BeautifulSoup:
    """
    Parameters:
    url: str supeを作る対象のurl

    Returns:
    BeautifulSoup
    """
    try:
        print("supeの作成")
        res = requests.get(url, headers=headers_pc)
        html = res.text
        supe = BeautifulSoup(html, "html.parser")
        return supe
    except Exception as e:
        print(f'failed to create supe:{e}')
        return None


# ! ページ数の取得
def get_page_count(url: str) -> int:
    try:
      print("ページ数の取得開始")
      supe = create_supe(url)
      shop_count = supe.find("div", {"class": "list_search_list_counter"}).select("p")[1].find("span").text.strip()
      print("ページ数取得")
      #! 歯医者の件数
      shop_count = int(shop_count.replace(",",""))
      #! ページ総数
      page_count = math.ceil(shop_count / 20)
      return page_count
    except Exception as e:
      print(f'failed get pages count:{e}')
      return None

#! 1ページに表示されている歯医者のページURL(20件)を取得
def get_dental_url_list(page_url: str) -> list:
    """
    Parameters:
    page_url (str): 各歯科医院が表示(20件)されているページURL

    Returns:
    list: 各歯科医院のURLリスト
    """
    try:
        print("歯医者のページURL(20件)を取得")
        supe = create_supe(page_url)
        dental_li_list = supe.find("div", {"class": "list_search_casette_wrap"}).select(".list_search_casette_solo_box")
        dental_url_list = [dental_url.find("h2").find("a").get("href") for dental_url in dental_li_list]
        return dental_url_list
    except Exception as e:
        print(f'failed get urls:{e}')
        return None

#!歯医者のページからデータを取得
def get_dental_info(dental_url: str) -> list:
    """
    Parameters:
    dental_url (str): 歯医者の個別ページURL

    Returns:
    list: 各種取得した値をリストで返す
    """
    print("歯医者のページからデータを取得開始")
    supe = create_supe(dental_url)

    try:
      #! 名前
      name = supe.find("h1", {"class": "name_main"}).text.strip()
      cleaned_name = name.replace("　", " ")

      #! 電話番号
      phone_column = supe.select(".infomation_telephone")
      if phone_column:
        phone = phone_column[0].text.strip()
      else:
        phone = None

      #! 診療項目
      medical_treatment_column = supe.select(".detail_top_subject_wrap")
      if medical_treatment_column:
        medical_treatment_with_tag_list = medical_treatment_column[0].select("span")
        medical_treatment_list = [medical_treatment.text.strip() for medical_treatment in medical_treatment_with_tag_list]
      else:
        medical_treatment_list = []

      #! サーピス
      div_list = supe.find_all("div", {"class": "area_section-detail02"})
      target_div = div_list[len(div_list) - 1]
      service_column = target_div.find(text="サービス")
      if service_column:
        service_list = service_column.parent.parent.find("td").text.strip().split("｜")
      else:
        service_list = []


      #! 院長名 or 理事長名
      supe2 = create_supe(f"{dental_url}tab/4/")
      staff_column_list = supe2.find_all("h3", {"class": "staff_role_title"})
      if staff_column_list:
        chairman = [column for column in staff_column_list if "理事長" in column.text]
        director = [column for column in staff_column_list if "院長" in column.text]
        if director:
            representive = director[0].find("p").text.strip().replace("　", " ")
        elif chairman:
            representive = chairman[0].find("p").text.strip().replace("　", " ")
        else:
            #! 院長・理事長表記されてないがスタップ紹介がある場合は一番上の人を取得
            representive = staff_column_list[0].find("p").text.strip().replace("　", " ")
      else:
        representive = None

      result = [
          cleaned_name,
          representive,
          phone,
          service_list,
          medical_treatment_list,
      ]

      return result
    except Exception as e:
      print(f'failed get data from dental website:{e}')
      return None


# ! 実行関数
def run(url: str):
  """
  Returns:
  list: csvに変換する為のファイル構成で返す
  >>>example
  [["データ1"],["データ2"],["データ3"]]
  """
  test_box = []
  print("run")
  url_list = get_dental_url_list(url)
  data = list(tqdm(map(get_dental_info, url_list), desc="データ取得:", total=len(url_list)))
  row = ["名前", "院長・理事長", "電話番号", "サービス", "診療項目"]
  for_csv_data = [row, *data]
  # for info in tqdm(url_list, desc="データ取得", total=len(url_list)):
  #   print("a")
  #   test_box = [*test_box, get_dental_info(info)]
  return for_csv_data


#! チェック用
def abc():
  url = "https://haisha-yoyaku.jp/bun2sdental/detail/index/id/1330388595/tab/4/"
  supe2 = create_supe("https://haisha-yoyaku.jp/bun2sdental/detail/index/id/1330388595/tab/4/")
  staff_column_list = supe2.find_all("h3", {"class": "staff_role_title"})
  if staff_column_list:
    chairman = [column for column in staff_column_list if "理事長" in column.text]
    director = [column for column in staff_column_list if "院長" in column.text]
    if director:
        representive = director[0].find("p").text.strip().replace("　", " ")
    elif chairman:
        representive = chairman[0].find("p").text.strip().replace("　", " ")
    else:
        representive = None
  else:
    representive = None

  print(representive)


#! csv保存
def save_to_csv(data_list: list, page_num: int) -> None:

  try:
    #! csv保存先のディレクトリを作成
    directory_path = "/flask/dist/csv"
    tz = pytz.timezone('Asia/Tokyo')
    today_date = datetime.now(tz)
    format_folder_name = today_date.strftime("%Y%m%d")
    today_directory_path = os.path.join(directory_path, format_folder_name)

    #! csvファイル名の作成
    format_csv_file_name = today_date.strftime("%Y%m%d%H%M%S")
    csv_file_name = f"page_{page_num}_{format_csv_file_name}.csv"
    csv_path = os.path.join(today_directory_path, csv_file_name)
    create_directory_if_not_exists(today_directory_path)
    with open(csv_path, "w", newline='') as csvfile:
      csv_writer = csv.writer(csvfile)
      for row in data_list:
        converted_row = []
        for item in row:
          if isinstance(item, list):
            converted_row.append(','.join(item))
          else:
            converted_row.append(item)
        csv_writer.writerow(converted_row)
  except Exception as e:
    print(f'failed save csv file: {e}')

#! フォルダの作成
def create_directory_if_not_exists(directory_path):
  if not os.path.exists(directory_path):
      os.makedirs(directory_path)