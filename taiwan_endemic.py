import pandas as pd
import numpy as np

df = pd.read_excel("C:\\Users\\aleks\\Downloads\\台灣特有動物.xlsx")
df.info()

df['觀測年'] = df['觀測年'].astype(str)
df['觀測月'] = df['觀測月'].astype('Int64').astype(str)
df['觀測日'] = df['觀測日'].astype('Int64').astype(str)

df['原始座標誤差(公尺)'] = df['原始座標誤差(公尺)'].astype('Int64').astype(str)

# Drop columns with more than 90% missing values
df = df.dropna(axis=1,thresh=0.1*len(df))

# Select the top 15 most frequently observed species
top_15 = df['分類群俗名'].value_counts().head(15).index
df_top_15 = df[df['分類群俗名'].isin(top_15)]
df_top_15['分類群俗名'].nunique()

df_top_15['分類群俗名'].value_counts()

# Standardize species names
df_top_15['分類群俗名'] = df_top_15['分類群俗名'].replace({
    '鼬獾(subaurantiaca亞種)': '鼬獾',
    '臺灣野豬(taivanus亞種)': '臺灣野豬',
    '赤腹松鼠(thaiwanensis亞種)': '赤腹松鼠',
    '白鼻心(taivana亞種)': '白鼻心',
    '黃喉貂(chrysospila亞種)': '黃喉貂'
})
df_top_15['分類群俗名'] = df_top_15['分類群俗名'].str.strip()

def assign_emoji(species):
    emoji_dict = {
        '臺灣山羌':'🦌',
        '臺灣獼猴':'🐒',
        '臺灣水鹿':'🦌',
        '臺灣野山羊':'🐐',
        '鼬獾':'🐀',
        '臺灣刺鼠':'🐹',
        '臺灣野豬':'🐗',
        '臺灣黑熊':'🐻',
        '臺灣梅花鹿':'🦌',
        '赤腹松鼠':'🐿️',
        '白鼻心':'🐀',
        '臺灣野兔':'🐇',
        '高山白腹鼠':'🐁',
        '黃喉貂':'🦦',
        '臺灣森鼠':'🐭'      
    }
    return emoji_dict.get(species,'❓')

df_top_15['emoji'] = df_top_15['分類群俗名'].apply(assign_emoji)

def english_translate(species):
    english_dict = {
        '臺灣山羌': 'Formosan Muntjac',
        '臺灣獼猴': 'Formosan Rock Macaque',
        '臺灣水鹿': 'Formosan Sambar Deer',
        '臺灣野山羊': 'Formosan Serow',
        '鼬獾': 'Formosan Ferret-Badger',
        '臺灣刺鼠': "Coxing's White-Bellied Rat",
        '臺灣野豬': 'Formosan Wild Boar',
        '臺灣黑熊': 'Formosan Black Bear',
        '臺灣梅花鹿': 'Formosan Sika Deer',
        '赤腹松鼠': 'Red-Bellied Tree Squirrel',
        '白鼻心': 'Masked Palm Civet',
        '臺灣野兔': 'Formosan Hare',
        '高山白腹鼠': 'Formosan White-Bellied Rat',
        '黃喉貂': 'Formosan Yellow-Throated Marten',
        '臺灣森鼠': 'Formosan Field Mouse'
    }
    return english_dict.get(species, '❓')

df_top_15['分類群俗名_英文'] = df_top_15['分類群俗名'].apply(english_translate)

def explain(species):
    explain_dict = {
        '臺灣山羌': "The Formosan Mmuntjac is one of three deer species native to Taiwan. It is a small member of the deer family, with a body length of about 47-70 cm, weighing around 5-12 kg.The back of its body is dark yellow, while the upper chest and sides are gray-brown. Its limbs are dark brown, and the sides of the head, neck, throat, and lower chest are yellowish-brown. Females do not have antlers, while males have a pair of simple, forked antlers with small ridges in front of the antler base.",
        '臺灣獼猴': "The Formosan rock macaque, also known as the Formosan rock monkey or Taiwanese macaque, is a macaque endemic to Taiwan, which has also been introduced to Japan. Formosan rock macaques are the only native primates living in Taiwan. 壽山 Shoushan, a hill in southern Taiwan’s Kaohsiung city, is their best-known habitat.",
        '臺灣水鹿': "Formosan sambar deer's main habitat is in the mountains of Taiwan woodland. Wild Taiwan sambar still exist, but the number is minimal. Sambar deer are Taiwan's largest herbivores, with a head and body length approximating 180 cm. They are also known as “four-eyed deer” because of their suborbital glands, which are situated just below their eyes. Its fur color changes with season to provide camouflage. It is yellowish-brown in the summer and dark brown in the winter.",
        '臺灣野山羊': "The Formosan serow, also known as the Taiwan serow, is Taiwan's only known native bovid. It is widely distributed throughout the island's mountainous regions. This species is adapted to steep and rugged terrain, where its special hoofs enable it to move freely about rocky slopes and cliffs.",
        '鼬獾': "The Formosan ferret-badger, endemic to Taiwan, is a distinct species, not a subspecies of the Chinese ferret-badger, despite sharing badger-like features like short legs, broad paws, and long claws for digging.",
        '臺灣刺鼠': "Coxing's white-bellied rat is the species was first described by Robert Swinhoe in 1864 and is endemic to Taiwan. It occurs in broad-leaf forests and their edges and in scrub. It is more common at elevations below 1,300 m but can be found up to 2,000 m.",
        '臺灣野豬': "The Taiwan wild boar is native to Taiwan. It is a unique subspecies that has adapted to live in the coastal plains of Taiwan and in the mountains 3,000 meters above sea level.",
        '臺灣黑熊': "The Formosan black bear is one of the seven subspecies of Ursus thibetanus formosanus endemic to Taiwan and is considered an endangered wild animal. At present, there are only about 200 to 600 of them left in Taiwan.",
        '臺灣梅花鹿': "Formosan sika deer is a subspecies of sika deer endemic to the island of Taiwan. Sika stand 90–120 cm at the shoulder, 155 cm in length, 43–68 kg in weight. The natural distribution of sika on Taiwan was in the woodlands from sea level up to about 300 meters elevation. Sika, like many deer, prefer areas of mixed forest, scrub, and open land.",
        '赤腹松鼠': "Pallas's squirrel, or Red-Bellied Tree Squirrel, is found throughout much of southeastern Asia. s a medium-sized tree squirrel, with a head-body length of 16 to 28 cm, and a tail 11 to 26 cm in length.",
        '白鼻心': "The masked palm civet is a viverrid species native to the Indian subcontinent and Southeast Asia. It has been listed as least concern on the IUCN Red List since 2008 as it occurs in many protected areas.The Formosan masked palm civet has a black head with a distinct white stripe from the forehead to the nose. Their claws are retractable, making it a tree-climbing master. Their anal glands can release foul-smelling scent to scare away the predators. The natural habitats are depleting due to many human and environmental reasons.",
        '臺灣野兔': "Formosan Hares used to distribute from plains to the regions in altitude of 500 meters. However, nowadays both the plains and hills of Taiwan have been over-developed. The Formosan hares have lost their original natural habitat and moved into the mountains. Their population has been decreased.",
        '高山白腹鼠': "The Formosan white-bellied rat, scientifically known as Niviventer culturatus, is a species of rodent endemic to Taiwan.",
        '黃喉貂': "The Formosan yellow-throated marten is a yellow and brown short-haired omnivore dwelling in mountain forests below 2,000 meters, though a few have settled at 3,850 meters in the woods near the North Peak Weather Station on 玉山 Yushan. They look cute and small, but their claws and teeth make them deadly hunters, occasionally preying on mammals larger than they are.",
        '臺灣森鼠': "The Taiwan field mouse is found only in Taiwan. It is primarily distributed in the montane region between 1,400 and 3,000 m. They inhabit various habitat types, such as natural or planted forests, grasslands, farms, and campsites, and are omnivorous feeding on plants, insects and fungi."
    }
    return explain_dict.get(species, '❓')

df_top_15['說明'] = df_top_15['分類群俗名'].apply(explain)

def image(species):
    image_dict = {
        '臺灣山羌': 'https://taieol.tw/files/muse_taieol/muse_styles/w1024/mcode/999994c175cba7471ab1a827effae27d.jpg?itok=5N6ISGXu',
        '臺灣獼猴': 'https://taieol.tw/files/muse_taieol/muse_styles/w1024/mcode/0478fab2b505a44b832e01efa8118815.jpg?itok=9nffwTO8',
        '臺灣水鹿': 'https://taieol.tw/files/muse_taieol/muse_styles/w1024/mcode/8c6a6f835b9d58ec88e0da97eae5de9b.jpg?itok=1gR-jAfr',
        '臺灣野山羊': 'https://taieol.tw/files/muse_taieol/muse_styles/w1024/mcode/5f80ea685b89871f9019e665cf62ceef.jpg?itok=S1QJO6Iq',
        '鼬獾': 'https://taieol.tw/files/muse_taieol/muse_styles/w1024/mcode/7fae8db90adeb2b32cbe999d14f246e9.jpg?itok=7AKXHDLF',
        '臺灣刺鼠': "https://taieol.tw/files/muse_taieol/muse_styles/w1024/mcode/a964933481ad59419928e51ba3441119.jpg?itok=XSQCcAQJ",
        '臺灣野豬': 'https://taieol.tw/files/muse_taieol/muse_styles/color_box_match/mcode/3021a05fc1ba8ff0aa78f780af758918.jpg?itok=731P7llI',
        '臺灣黑熊': 'https://www.taiwanbear.org.tw/admin/resource/images/f5cec9392d534b.jpeg',
        '臺灣梅花鹿': 'https://taieol.tw/files/muse_taieol/muse_styles/color_box_match/mcode/21a2e9c5e1ea043a6f72b6b9808d17fa.jpg?itok=l8NuGUmz',
        '赤腹松鼠': 'https://taieol.tw/files/muse_taieol/muse_styles/w1024/mcode/d6feda4f61cf5cd4e3947e2b59769606.jpg?itok=7V5XaDtx',
        '白鼻心': 'https://taieol.tw/files/muse_taieol/muse_styles/w1024/mcode/6d46c86f418ff560392166088e7dfdaa.jpg?itok=kJ00OQMY',
        '臺灣野兔': 'https://taieol.tw/files/muse_taieol/muse_styles/w1024/mcode/0a904c85cbfeec15fe1f2e1b98979c91.jpg?itok=hFyrAzzS',
        '高山白腹鼠': 'https://taieol.tw/files/muse_taieol/muse_styles/w1024/mcode/3c6473ed423777965cb64e09e0cbd9ad.jpg?itok=wfFO_OwR',
        '黃喉貂': 'https://taieol.tw/files/muse_taieol/muse_styles/w1024/mcode/25597e4f6f3a811fe0b1ff56d7eca035.jpg?itok=m39APp7N',
        '臺灣森鼠': 'https://taieol.tw/files/muse_taieol/muse_styles/w1024/mcode/fb331726220514856cbee66f8976da43.jpg?itok=64oBbV3K'
    }
    return image_dict.get(species, '❓')

df_top_15['照片'] = df_top_15['分類群俗名'].apply(image)

# Get the most frequently observed administrative regions for each species
df_grouped = df_top_15.groupby('分類群俗名')['行政區'].value_counts().groupby(level=0).head(4)

# Extract representative location and metadata for each species-region pair
df_mode = (
    df_top_15.groupby(['分類群俗名', '行政區'])[['緯度(十進位)', '經度(十進位)', '分類群俗名', '行政區','emoji', '分類群俗名_英文', '說明', '照片', '國內紅皮書']]
    .apply(lambda x: x.mode().iloc[:1] if not x.mode().empty else x.iloc[:1])
    .reset_index(drop=True)
)

df_grouped = df_grouped.reset_index()
df_grouped = df_grouped.merge(
    df_mode[['分類群俗名', '行政區', '緯度(十進位)', '經度(十進位)','emoji','分類群俗名_英文', '說明', '照片','國內紅皮書']],
    on=['分類群俗名', '行政區'],  
    how='left'  
)

df_grouped['國內紅皮書'].value_counts()

import folium

min_lon, max_lon = 119.083484, 122.842401
min_lat, max_lat = 21.928963, 25.155479

map = folium.Map(
    location=[24.265432, 121.187712],
    zoom_start=10,
    tiles='CartoDB Voyager',
    max_bounds=True,
    min_lat=min_lat,
    max_lat=max_lat,
    min_lon=min_lon,
    max_lon=max_lon
)

# Add Google Maps tile layer
google_maps = folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
    attr='Google Maps',
    name='Google Maps in Chinese'
)
google_maps.add_to(map)

# Add color mapping for conservation status
red_list_colors = {
    '暫無危機（LC, Least Concern）': 'green',
    '不適用': 'gray',
    '接近受脅（NT, Near Threatened）': 'orange',
    '瀕危（EN, Endangered）': 'darkred',
    '易危（VU, Vulnerable）': 'red'
}

# Ensure df_grouped exists
for idx, row in df_grouped.iterrows():
    name = row['分類群俗名']
    description = row.get('行政區', '無資料')
    emoji = row['emoji']
    english = row['分類群俗名_英文']
    about = row['說明']
    image = row['照片']
    danger = row['國內紅皮書']

    lat, lon = offset_coordinates(row['緯度(十進位)'], row['經度(十進位)'])

    # Assign color based on conservation status
    danger_color = red_list_colors.get(danger, 'black')

    popup_content = f"""
    <b style='font-size: 24px;'>{name} {english}</b><br>
    <img src="{image}" alt="{name}" style="width: 100%; height: auto; border-radius: 14px; margin:18px 0;"><br>
    <b style='font-size: 16px;'>行政區:</b> {description}<br>
    <p style='font-size: 16px;'>{about}</p>
    <b style='font-size: 16px; color: {danger_color};'>國內紅皮書狀態:</b> {danger if danger else '未列入'}<br>
    """

    # Create marker with emoji icon
    marker = folium.Marker(
        location=[lat, lon],
        icon=folium.DivIcon(html=f"<div style='font-size: 24px'>{emoji}</div>")
    )

    popup = folium.Popup(popup_content, max_width=400)
    marker.add_child(popup)
    marker.add_to(map)  

map
map.save('臺灣特有動物.html')
