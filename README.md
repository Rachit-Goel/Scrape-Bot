# Scrape-Bot
A chatbot inside a Chrome extension that can scrape all text from the current active page and store the text content on a database. It can search text over all stored content from databse and shows snippets as results.

### Tech Stack Used
FastAPI Python Backend, VueJS for Frontend (Vue3 with Vite build tool), Supabase for PostgreSQL Database, BeautifulSoup for web-scraping.

### How to run in local

#### Clone repo 
    git clone https://github.com/Rachit-Goel/Scrape-Bot.git

#### To run Server
In the directory, "Scrape-Bot":

- Use python 3.10.0, can manage\install versions using pyenv & create new virtual environment using venv, then run command  
    ```
    pip install -r requirements.txt
    ```
    
- Then run server using uvicorn, run command
    ```
    uvicorn main:app --reload
    ```


#### To run Chrome Extension
- In another terminal, come inside the directory, "Scrape-Bot\scrape-bot":
    ```
    cd .\scrape-bot\
    ```

- Install all packages for the frontend, run command: 
    ```
    npm install
    ```

- Run build command, this will create dist folder: 
    ```
    npm run build
    ```
    Note: If you try to run as a web app using "npm run dev" then while scraping chrome API will not work in Vue, it works in chrome extension only. For web app you can comment chrome API code and use "window.location.href" to get the current active tab's url.

- Add "manifest.json" file in "Scrape-Bot\scrape-bot\dist" folder: 
    ```
    {
      "manifest_version": 3,
      "name": "Srape-Bot",
      "description": "",
      "version": "1.0.0",
      "permissions": ["bookmarks", "activeTab", "tabs", "storage"],
      "action": {
          "default_popup": "index.html"
      }
    }
    ```

- Then, in Chrome Browser open "chrome://extensions/", turn developer mode on, click on "Load Unpacked" browse path & select 'dist' folder inside "Scrape-Bot\scrape-bot" directory, pin the "Scrape-Bot" extension.

- Now you open any website (https://example.com/) for which you want to scrape all text content, click on extension choose button to scrape current page or search any text query.

  Note: Make sure backend server is running on: http://127.0.0.1:8000. Otherwise we need to change server url for API request in app.vue file.
