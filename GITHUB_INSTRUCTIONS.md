# Як викласти проєкт на GitHub (приватний репозиторій) і оновлювати після змін

**Ваш репозиторій:** https://github.com/danildocenko2000-sketch/Pogooda-

---

## Швидко (після встановлення Git)

1. **Перше завантаження** — запустіть у папці `Pogoda` файл **`git_first_upload.bat`**. Він ініціалізує репозиторій, додасть remote і відправить код на GitHub. При запиті логіну використовуйте **Personal Access Token** (GitHub → Settings → Developer settings → Personal access tokens).
2. **Після кожних змін** — запустіть **`git_push.bat`**. Введіть короткий опис змін і натисніть Enter — зміни відправляться на GitHub.

---

## Крок 0. Встановити Git (якщо ще немає)

1. Завантажте Git для Windows: https://git-scm.com/download/win  
2. Встановіть (можна залишити стандартні опції).  
3. Перезапустіть термінал (або Cursor). Перевірка: відкрийте PowerShell і введіть `git --version` — має з’явитися версія.

---

## Крок 1. Обліковий запис GitHub

1. Зареєструйтеся на https://github.com (або увійдіть).  
2. Для приватного репозиторія достатньо безкоштовного акаунта.

---

## Крок 2. Створити **приватний** репозиторій на GitHub

1. У правому верхньому куті натисніть **"+"** → **"New repository"**.  
2. **Repository name:** наприклад `pogoda` або `gidro-term-pogoda`.  
3. **Visibility:** оберіть **Private**.  
4. **НЕ** ставте галочки "Add a README", "Add .gitignore", "Choose a license" — репозиторій має бути порожнім.  
5. Натисніть **"Create repository"**.  
6. На сторінці репозиторія скопіюйте URL, наприклад:  
   `https://github.com/ВАШ_ЛОГІН/pogoda.git`

---

## Крок 3. Перше завантаження проєкту (один раз)

Відкрийте **PowerShell** або **Command Prompt** і виконайте команди по черзі. Замість `E:\gidro_term\Pogoda` підставте свій шлях до папки проєкту, замість `https://github.com/ВАШ_ЛОГІН/pogoda.git` — URL вашого репозиторія.

```powershell
cd E:\gidro_term\Pogoda
```

Ініціалізувати репозиторій:

```powershell
git init
```

Додати віддалений репозиторій (замініть URL на свій):

```powershell
git remote add origin https://github.com/ВАШ_ЛОГІН/pogoda.git
```

Перевірити, що все ігнорується з `.gitignore` (node_modules, __pycache__, .env, dist тощо не потраплять у репозиторій). Далі — перший коміт і відправка:

```powershell
git add .
git status
git commit -m "Перше завантаження: Pogoda (backend, weather, admin)"
git branch -M main
git push -u origin main
```

- Якщо GitHub попросить логін/пароль: пароль **не** підходить — потрібен **Personal Access Token (PAT)**.  
- Створити токен: GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)** → **Generate new token**. Дозвольте доступ до репозиторіїв (repo). Скопіюйте токен і вставте замість пароля при `git push`.

Після успішного `git push` проєкт з’явиться в приватному репозиторії на GitHub.

---

## Крок 4. Після кожних змін — завантажити оновлення на GitHub

Кожного разу, коли щось змінили в проєкті і хочете зберегти це на GitHub:

```powershell
cd E:\gidro_term\Pogoda
git add .
git status
git commit -m "Короткий опис змін"
git push
```

- **`git add .`** — додає всі зміни (нові, змінені, видалені файли).  
- **`git status`** — показує, що саме потрапить у коміт (корисно переглянути).  
- **`git commit -m "..."`** — фіксує зміни з коротким описом (наприклад: "Додано сторінку налаштувань", "Виправлено API погоди").  
- **`git push`** — відправляє коміти на GitHub.

Якщо працюєте в гілці **main** і вже виконували `git push -u origin main`, далі достатньо просто **`git push`**.

---

## Корисні команди

| Команда | Що робить |
|--------|------------|
| `git status` | Що змінено і що вже додано до коміту |
| `git add .` | Додати всі зміни |
| `git add папка/` | Додати тільки зміни в папці |
| `git commit -m "текст"` | Зробити коміт з описом |
| `git push` | Відправити коміти на GitHub |
| `git pull` | Завантажити зміни з GitHub (якщо правите з іншого ПК) |

---

## Якщо репозиторій створювали з README на GitHub

Якщо при створенні репозиторія ви додали README, перед першим `git push` виконайте:

```powershell
git pull origin main --allow-unrelated-histories
```

Потім знову:

```powershell
git push -u origin main
```

---

## Короткий чеклист після змін

1. Відкрити термінал у папці проєкту: `cd E:\gidro_term\Pogoda`  
2. `git add .`  
3. `git commit -m "Опис змін"`  
4. `git push`

Після цього усі останні зміни будуть на GitHub у вашому приватному репозиторії.
