import re

# Fayl adları (Birbaşa .csv formatında işləyir)
orijinal_ingilis_fayli = 'en.csv'
deep_tercume_fayli = 'az_deepl.csv'
yeni_duzelmis_fayl = 'az_final_hizalanmis.csv'

print("1. Orijinal İngilis dili (.csv) strukturu və boşluqları oxunur...")
with open(orijinal_ingilis_fayli, 'r', encoding='utf-8') as f:
    en_setirler = f.readlines()

print("2. DeepL-dən gələn qarışmış Azərbaycan dili mətni oxunur...")
with open(deep_tercume_fayli, 'r', encoding='utf-8') as f:
    deepl_metni = f.read()

# DeepL-in mətni təmizlənir, lakin oyun kodları qorunur
deepl_metni_temiz = re.sub(r'\s+', ' ', deepl_metni)

yeni_csv_iceriyi = []
xeta_sayi = 0

print("3. İngilis dili bazası əsasında milimetrik hizalanma və bərpaya başlanıldı...")

for setir in en_setirler:
    # Başlıq sətirlərini (;meta və s.) olduğu kimi qoruyuruq
    if setir.startswith(';') or not setir.strip():
        yeni_csv_iceriyi.append(setir)
        continue
    
    # Sətirin əvvəlindəki orijinal boşluqları (indentation) milimetrik olaraq götürürük
    baslangic_bosluqlari = setir[:len(setir) - len(setir.lstrip())]
    
    hisseler = setir.split('|')
    if len(hisseler) >= 4:
        id_num = hisseler[0].strip()
        hex_num = hisseler[1].strip()
        keystr = hisseler[2].strip()
        orijinal_text = hisseler[3].strip()
        
        # Əgər İngilis dilində bu ID-nin qarşısı boşdursa, elə boş saxlayırıq
        if not orijinal_text:
            yeni_csv_iceriyi.append(f"{baslangic_bosluqlari}{id_num}|{hex_num}|{keystr}|\n")
            continue
            
        # REGEX FƏNDİ: DeepL-in qarışdırdığı mətnin içində bu ID-ni axtarırıq.
        # Əgər bu ID başqa bir sözün arxasına yapışıbsa belə (\s* və ya bitişik), 
        # kod onu ordan tapır, qoparır və aşağı sətirə salır.
        pattern = rf"{id_num}\s*\|\s*{hex_num}\s*\|\s*{keystr}\s*\|(.*?)(?=\s*\d+\s*\||$)"
        match = re.search(pattern, deepl_metni_temiz)
        
        if match:
            az_text = match.group(1).strip()
            # Orijinal İngilis dili boşluqları və ID-si ilə Azərbaycan mətnini birləşdiririk
            yeni_csv_iceriyi.append(f"{baslangic_bosluqlari}{id_num}|{hex_num}|{keystr}|{az_text}\n")
        else:
            # Əgər DeepL bu ID-ni tamamilə məhv edibsə, oyunun çökməməsi üçün
            # bura köhnə DIQQET yazımızı qoyuruq və yanına İngilis mətni yazırıq ki, harada xəta var biləsiniz.
            xeta_sayi += 1
            yeni_csv_iceriyi.append(f"{baslangic_bosluqlari}{id_num}|{hex_num}|{keystr}|[DIQQET: Tercume İtib və ya Birləsib] {orijinal_text}\n")

# Yeni .csv faylını yazırıq
with open(yeni_duzelmis_fayl, 'w', encoding='utf-8') as f:
    f.writelines(yeni_csv_iceriyi)

print("\n==================================================")
print(f"UĞURLU! Yeni fayl yaradıldı: {yeni_duzelmis_fayl}")
print(f"İngilis dili ID-ləri və boşluqları 100% bərpa olundu.")
print(f"Birləşən sətirlər aşağı çəkildi. Cəmi {xeta_sayi} sətirdə [DIQQET] bərpası lazım oldu.")
print("==================================================")
