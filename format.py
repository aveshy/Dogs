import pandas as pd
import numpy as np

# Указание пути к исходному файлу и пути для сохранения отформатированного файла
input_file_path = 'dog_breeds.csv'
output_file_path = 'formatted_dog_breeds.csv'

# Чтение исходного датасета
df = pd.read_csv(input_file_path)

# Удаление дубликатов на основании столбца 'Breed'
df = df.drop_duplicates(subset=['Breed'])

# Перевод высоты из дюймов в сантиметры и разделение на минимальную и максимальную высоту
def convert_height(height):
    min_height, max_height = map(lambda x: int(x) * 2.54, height.split('-'))
    return min_height, max_height

df[['Min Height (cm)', 'Max Height (cm)']] = df['Height (in)'].apply(convert_height).apply(pd.Series)
df.drop(columns=['Height (in)'], inplace=True)

# Разделение столбца Longevity на min и max
def split_longevity(longevity):
    min_longevity, max_longevity = map(int, longevity.split('-'))
    return min_longevity, max_longevity

df[['Min Longevity (yrs)', 'Max Longevity (yrs)']] = df['Longevity (yrs)'].apply(split_longevity).apply(pd.Series)
df.drop(columns=['Longevity (yrs)'], inplace=True)

# Словари для перевода
characters_translation = {
    'active': 'Активный', 'affectionate': 'Ласковый', 'athletic': 'Атлетичный',
    'brave': 'Храбрый', 'calm': 'Спокойный', 'charming': 'Очаровательный',
    'confident': 'Уверенный', 'curious': 'Любопытный', 'energetic': 'Энергичный',
    'friendly': 'Дружелюбный', 'gentle': 'Кроткий', 'good-natured': 'Добродушный',
    'hypoallergenic': 'Гипоаллергенный', 'independent': 'Независимый', 'intelligent': 'Умный',
    'kind': 'Милый', 'loyal': 'Верный', 'patient': 'Терпеливый', 'playful': 'Игривый',
    'protective': 'Собака-охранник', 'sensitive': 'Чувствительный', 'social': 'Социальный',
    'strong': 'Сильный', 'trainable': 'Обучаемый'}

health_problems_translation = {
    'bladder stones': 'Камни в мочевом пузыре', 'breathing problems': 'Проблемы с дыханием',
    'cancer': 'Рак', 'dental problems': 'Проблемы с зубами', 'diabetes': 'Диабет',
    'ear infections': 'Ушные инфекции', 'elbow dysplasia': 'Дисплазия локтевого сустава',
    'epilepsy': 'Эпилепсия', 'eye issues': 'Глазные заболевания', 'eye problems': 'Проблемы со зрением',
    'heart conditions': 'Сердечные заболевания', 'hereditary myopathy': 'Наследственная миопатия',
    'hip dysplasia': 'Дисплазия тазобедренного сустава', 'intervertebral disc disease': 'Заболевание межпозвоночного диска',
    'obesity': 'Ожирение', 'pancreatitis': 'Панкреатит', 'respiratory issues': 'Респираторные заболевания',
    'skin allergies': 'Кожные аллергии'}

eyes_color_translation = {'Brown': 'Карий', 'Blue': 'Голубой', 'Grey': 'Серый'}

fur_color_translation = {'Apricot': 'Персиковая', 'Black': 'Черная', 'Black & Tan': 'Черная с подпалым', 'Black & White': 'Черно-белая',
    'Blenheim': 'Окрас Блейнхем', 'Blue': 'Голубая', 'Blue & Tan': 'Голубая с подпалым', 'Blue Merle': 'Окрас Блю-Мерль',
    'Brindle': 'Тигрово-полосатый окрас', 'Brown': 'Коричневая', 'Chocolate': 'Шоколадная', 'Cream': 'Кремовый окрас',
    'Fawn': 'Олений окрас', 'Gold': 'Золотой окрас', 'Golden': 'Золотистый окрас', 'Grey': 'Серая', 'Harlequin': 'Мраморный окрас',
    'Lemon': 'Лимонный окрас', 'Light Wheaten': 'окрас Керн Терьера', 'Liver': 'Ливерный окрас', 'Mahogany': 'Окрас Красное дерево',
    'Merle': 'Окрас Мерль', 'Orange': 'Оранжевая', 'Pink': 'Розовый окрас', 'Red': 'Рыжая', 'Sable': 'Окрас шарпея',
    'Salt & Pepper': 'Окрас Перец с солью', 'Sesame': 'Кунжутный окрас', 'Silver': 'Серебристый окрас', 'Stag Red': 'Красно-коричневая',
    'Tan': 'Подпалая', 'Wheaten': 'Окрас Терьера', 'White': 'Белая', 'Yellow': 'Желтая'}

country_translation = {'Canada': 'Канада', 'Germany': 'Германия', 'England': 'Англия', 'France': 'Франция',
    'Mexico': 'Мексика', 'Scotland': 'Шотландия', 'China': 'Китай', 'Russia': 'Россия', 'Australia': 'Австралия',
    'Switzerland': 'Швейцария', 'Ireland': 'Ирландия', 'Belgium': 'Бельгия', 'Rhodesia': 'Родезия',
    'United States': 'США', 'Madagascar': 'Мадагаскар', 'Italy': 'Италия', 'Wales': 'Уэльс', 'Middle East': 'Ближний Восток',
    'Finland': 'Финляндия', 'Japan': 'Япония', 'Netherlands': 'Нидерланды', 'Hungary': 'Венгрия', 'Tibet': 'Тибет',
    'Malta': 'Мальта', 'Turkey': 'Турция', 'Africa': 'Африка', 'Congo': 'Конго'}

dog_breeds_translation = {
    'Labrador Retriever': 'Лабрадор-ретривер', 'German Shepherd': 'Немецкая овчарка', 'Bulldog': 'Английский бульдог', 'Poodle': 'Пудель',
    'Beagle': 'Бигль', 'Chihuahua': 'Чихуахуа', 'Boxer': 'Боксер', 'Golden Retriever': 'Золотистый ретривер', 'Pug': 'Мопс',
    'Rottweiler': 'Ротвейлер', 'Siberian Husky': 'Сибирский хаски', 'Dachshund': 'Такса', 'Shih Tzu': 'Ши-тцу', 'Bichon Frise': 'Бишон фризе',
    'Australian Shepherd': 'Австралийская овчарка', 'Basset Hound': 'Бассет-хаунд', 'Cocker Spaniel': 'Кокер-спаниель',
    'French Bulldog': 'Французский бульдог', 'Pomeranian': 'Померанский шпиц', 'Great Dane': 'Немецкий дог', 'Mastiff': 'Мастиф',
    'Newfoundland': 'Ньюфаундленд', 'Saint Bernard': 'Сенбернар', 'Old English Sheepdog': 'Бобтейл',
    'Irish Wolfhound': 'Ирландский волкодав', 'Greyhound': 'Грейхаунд', 'Scottish Deerhound': 'Шотландский дирхаунд',
    'Great Pyrenees': 'Пиренейская горная собака', 'Shar Pei': 'Шарпей', 'Doberman Pinscher': 'Доберман-пинчер', 'Weimaraner': 'Веймаранер',
    'Belgian Malinois': 'Бельгийская овчарка Малинуа', 'Rhodesian Ridgeback': 'Родезийский риджбек', 'English Setter': 'Английский сеттер',
    'Pointer': 'Пойнтер', 'Gordon Setter': 'Шотландский сеттер', 'Irish Setter': 'Ирландский сеттер', 'Papillon': 'Папильон', 'Pekingese': 'Пекинес',
    'Toy Poodle': 'Той-пудель', 'Miniature Poodle': 'Карликовый пудель', 'Standard Poodle': 'Стандартный пудель', 'Affenpinscher': 'Аффенпинчер',
    'Boston Terrier': 'Бостон-терьер', 'Brussels Griffon': 'Брюссельский гриффон', 'Cairn Terrier': 'Керн-терьер',
    'Chinese Crested': 'Китайская хохлатая', 'Miniature Schnauzer': 'Цвергшнауцер', 'Standard Schnauzer': 'Миттельшнауцер',
    'West Highland White Terrier': 'Вест-хайленд-уайт-терьер', 'Australian Terrier': 'Австралийский терьер', 'Border Terrier': 'Бордер-терьер',
    'Coton de Tulear': 'Котон-де-тулеар', 'English Toy Spaniel': 'Английский той-спаниель',
    'Australian Stumpy Tail Cattle Dog': 'Австралийская короткохвостая пастушья собака', 'American Eskimo Dog': 'Американская эскимосская собака',
    'Australian Cattle Dog': 'Австралийская пастушья собака', 'Australian Kelpie': 'Австралийский келпи', 'Bloodhound': 'Бладхаунд',
    'Border Collie': 'Бордер-колли', 'American Bulldog': 'Американский бульдог', 'Borzoi': 'Борзая', 'Bull Terrier': 'Бультерьер',
    'Cane Corso': 'Кане Корсо', 'Cardigan Welsh Corgi': 'Вельш-корги кардиган', 'Chesapeake Bay Retriever': 'Чесапикский ретривер',
    'Saluki': 'Салюки', 'English Springer Spaniel': 'Английский спрингер-спаниель', 'Field Spaniel': 'Филд-спаниель',
    'Finnish Spitz': 'Финский шпиц', 'Flat-Coated Retriever': 'Прямошерстный ретривер', 'Giant Schnauzer': 'Ризеншнауцер',
    'Harrier': 'Харьер', 'Irish Terrier': 'Ирландский терьер', 'Irish Water Spaniel': 'Ирландский водяной спаниель',
    'Italian Greyhound': 'Левретка', 'Jack Russell Terrier': 'Джек-рассел-терьер', 'Japanese Chin': 'Японский хин', 'Keeshond': 'Кеесхонд',
    'Kerry Blue Terrier': 'Керри-блю-терьер', 'Kuvasz': 'Кувас', 'Lhasa Apso': 'Лхаса апсо', 'Maltese': 'Мальтийская болонка',
    'Miniature Pinscher': 'Карликовый пинчер', 'Samoyed': 'Самоед', 'Shetland Sheepdog': 'Шелти',
    'Staffordshire Bull Terrier': 'Стаффордширский бультерьер', 'Vizsla': 'Венгерская выжла', 'Anatolian Shepherd': 'Анатолийская овчарка',
    'Welsh Corgi': 'Вельш-корги', 'Welsh Springer Spaniel': 'Вельш-спрингер-спаниель', 'Welsh Terrier': 'Вельштерьер', 'Whippet': 'Уиппет',
    'Wirehaired Pointing Griffon': 'Гриффон Кортальса', 'Xoloitzcuintli': 'Ксолоитцкуинтли', 'Yorkshire Terrier': 'Йоркширский терьер',
    'Akita': 'Акита', 'Africanis': 'Африканис', 'Basenji': 'Басенджи', 'Catahoula Leopard Dog': 'Леопардовая собака Катахулы',
    'Miniature Shiba Inu': 'Карликовый сиба-ину', 'Belgian Tervuren': 'Бельгийский тервюрен', 'Pharaoh Hound': 'Фараонова собака'}

# Переводим значения
df['Breed'] = df['Breed'].map(dog_breeds_translation)
df['Country of Origin'] = df['Country of Origin'].map(country_translation)

df['Fur Color'] = df['Fur Color'].apply(lambda x: ', '.join([fur_color_translation[trait] for trait in x.split(', ')]))
df['Color of Eyes'] = df['Color of Eyes'].apply(lambda x: ', '.join([eyes_color_translation[trait] for trait in x.split(', ')]))

# Приведение к нижнему регистру
df['Character Traits'] = df['Character Traits'].str.lower()
df['Common Health Problems'] = df['Common Health Problems'].str.lower()
# Перевод значений в столбцах Character Traits и Common Health Problems с применением перевода
df['Character Traits'] = df['Character Traits'].apply(lambda x: ', '.join([characters_translation[trait] for trait in x.split(', ')]))
df['Common Health Problems'] = df['Common Health Problems'].apply(lambda x: ', '.join([health_problems_translation[problem] for problem in x.split(', ')]))

# Разъединение столбца Color of Eyes на новые столбцы с оригинальными значениями
character_traits_dummies = df['Character Traits'].str.get_dummies(sep=', ')
df = pd.concat([df, character_traits_dummies], axis=1)

health_problems_dummies = df['Common Health Problems'].str.lower().str.get_dummies(sep=', ')

# Функция для генерации случайных целых процентных значений, которые в сумме составляют 100%
def generate_random_integer_percents(num_problems):
    if num_problems == 0:
        return []
    random_values = np.random.randint(1, 100, num_problems)
    total = random_values.sum()
    random_percents = np.floor((random_values / total) * 100).astype(int)
    remainder = 100 - random_percents.sum()
    for i in range(remainder):
        random_percents[i % num_problems] += 1
    return random_percents

# Заполнение столбцов значениями в процентах (суммарно 100%)
for i, row in health_problems_dummies.iterrows():
    active_problems = row[row == 1].index
    percents = generate_random_integer_percents(len(active_problems))
    for problem, percent in zip(active_problems, percents):
        df.loc[i, problem] = percent

# Установка 0 для остальных проблем
for column in health_problems_dummies.columns:
    df[column] = df[column].fillna(0).astype(int)

# Удаление оригинальных столбцов, которые были разделены
df.drop(columns=['Character Traits', 'Common Health Problems'], inplace=True)

# Сохранение отформатированного DataFrame в новый CSV файл
df.to_csv(output_file_path, index=False)

print(f"Форматированный датасет сохранен по адресу: {output_file_path}")