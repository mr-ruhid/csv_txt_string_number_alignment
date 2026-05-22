import re

# FILE NAMES (You can change them to your own file names)
orijinal_turkce_fayl = 'tr.txt'         # Orijinal, düzgün strukturlu Türkcə faylınız
deep_tercume_fayli = 'az_deepl.txt'      # DeepL-dən gələn, sətirləri qarışmış Azərbaycan dili faylınız
duzelmis_fayl = 'az_hizalanmis.txt'     # Kodun çıxaracağı tam düzgün yeni fayl

print("Fayllar analiz edilir...")

# 1. orjinal fayildaki id-leri oyrenir
with open(orijinal_turkce_fayl, 'r', encoding='utf-8') as f:
    orijinal_setirler = f.readlines()

# 2. tercumeden gelen fayillari bir yere toplayir
with open(deep_tercume_fayli, 'r', encoding='utf-8') as f:
    deepl_metni = f.read()

# bosluqlari normallasdirma
# oyunun daxili <br> kodlarini qoruyuruq
deepl_metni_temiz = re.sub(r'\s+', ' ', deepl_metni)

yeni_fayl_iceriyi = []
son_tapilan_index = 0

print("Hizalanma və bərpa prosesi başladı...")

for setir in orijinal_setirler:
    # basliqlari saxlama
    if setir.startswith(';') or not setir.strip():
        yeni_fayl_iceriyi.append(setir)
        continue
    
    # setirlik hisselere bolme: ID | HEX | KeyStr | Text
    hisseler = setir.split('|')
    if len(hisseler) >= 4:
        id_num = hisseler[0].strip()
        hex_num = hisseler[1].strip()
        keystr = hisseler[2].strip()
        orijinal_text = hisseler[3].strip()
        
        # orjinalda metin yoxdursa ustunden kec
        if not orijinal_text:
            yeni_fayl_iceriyi.append(f"   {id_num}|{hex_num}|{keystr}|\n")
            continue
            
        # id axtarma
        # id uygunlasdirma
        pattern = rf"{id_num}\s*\|\s*{hex_num}\s*\|\s*{keystr}\s*\|(.*?)(?=\s*\d+\s*\||$)"
        match = re.search(pattern, deepl_metni_temiz)
        
        if match:
            az_text = match.group(1).strip()
            yeni_fayl_iceriyi.append(f"   {id_num}|{hex_num}|{keystr}|{az_text}\n")
        else:
            # tercumede itmis hisseleri tap
            # iki fayil arasinda problem varsa id itmir ancaq altdaki bildirisi alacaqssiniz
            yeni_fayl_iceriyi.append(f"   {id_num}|{hex_num}|{keystr}| [WARNING: There is a mistake here.] {orijinal_text}\n")

# fayl save
with open(duzelmis_fayl, 'w', encoding='utf-8') as f:
    f.writelines(yeni_fayl_iceriyi)

print(f"\nİş tamamlandı! Hizalanmış yeni faylınız hazır: {duzelmis_fayl}")
print("İndi Notepad++ ilə baxsanız, hər rəqəmin öz qarşısında öz mətni duracaq.")
