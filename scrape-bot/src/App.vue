/* eslint-disable */
<template>
  <div id="app">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else>
      <div v-if="showWelcomeMessage" class="message">
        <p>Welcome to the Chat-Bot!</p>
      </div>
      <div v-for="(chat, index) in chatHistory" :key="index" :class="chat.isBot ? 'bot-chat' : 'user-chat'">
        <div class="chat-message">
          <p>{{ chat.message }}</p>
        </div>
      </div>
      <div v-if="showOptions" class="options" id="container">
        <div>
          <button @click="handleScrapeClick">Scrape Current Page</button>
        </div>
        <div id="searchDiv">
          <input type="text" id="searchInput" placeholder="Search...">
          <button @click="handleSearchClick">Search</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      loading: false,
      showWelcomeMessage: true,
      showOptions: true,
      chatHistory: [],
    };
  },
  methods: {
    async handleScrapeClick() {
      this.showWelcomeMessage = false;
      this.showOptions = false;
      this.addUserChat("Scrape Current Page");
      this.loading = true;

      try {
        const activeTab = await this.getCurrentTab();
        const webpage = activeTab.url;
        console.log(webpage)

        if (!webpage) {
          this.addBotChat("Error: Could not get the current active page URL.");
          this.loading = false;
          this.showOptions = true;
          return;
        }

        const response = await axios.post("http://localhost:8000/scrape", {
          url: webpage,
        });

        if (response.status === 200) {
          this.addBotChat("Page scraped successfully!");
        } else {
          this.addBotChat("Error: Unable to scrape the page.");
        }
      } catch (error) {
        console.error(error);
        this.addBotChat("An error occurred while scraping the page.");
      }

      this.loading = false;
      this.showOptions = true;
    },
    async handleSearchClick() {
      this.showWelcomeMessage = false;
      this.showOptions = false;
      this.addUserChat("Search");
      
      try {
        const queryText = document.getElementById('searchInput').value.trim();
        if (!queryText) {
          this.addBotChat("Please enter a search query.");
          this.showOptions = true;
          return;
        }

        this.loading = true;
        const response = await axios.post("http://localhost:8000/search", {
          query: queryText,
        });

        if (response.status === 200) {
          this.addBotChat("Search results:");
          response.data.forEach((result) => {
            this.addBotChat(`- ${result.snippet}`);
          });
        } else {
          this.addBotChat("Error: Unable to perform the search.");
        }
      } catch (error) {
        console.error(error);
        this.addBotChat("An error occurred while performing the search.");
      }

      this.loading = false;
      this.showOptions = true;
    },

    getCurrentTab() {
        return new Promise((resolve, reject) => {
            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                const activeTab = tabs[0];
                if(activeTab){
                  resolve(activeTab);
                }
                else{
                  reject("There is an Error!");
                }
            });
        });
    },

    addBotChat(message) {
      this.chatHistory.push({ message, isBot: true });
    },

    addUserChat(message) {
      this.chatHistory.push({ message, isBot: false });
    },

  },
};
</script>

