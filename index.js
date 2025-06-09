require('dotenv').config();
const TelegramBot = require('node-telegram-bot-api');
const express = require('express');
const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');

const app = express();
app.use(express.json());

const GITHUB_REPO = process.env.GITHUB_REPO || 'hegdeshashank100/linkwala';
const GITHUB_FILE_PATH = process.env.GITHUB_FILE_PATH || 'links.json';
const GITHUB_TOKEN = process.env.GITHUB_TOKEN || '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';
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN || '7625370821:AAFvb_Yx5DF3v2U7KIF1ayM-Kn6-LfOkRMQ';
const JSON_FILE = 'links.json';
const PORT = process.env.PORT || 3000;

const bot = new TelegramBot(TELEGRAM_BOT_TOKEN, { polling: true });
let links = {};
const userStates = {};

const STATES = {
  ENTER_NAME: 1,
  ENTER_LINK: 2
};

async function loadLinksFromGitHub() {
  try {
    const url = `https://api.github.com/repos/${GITHUB_REPO}/contents/${GITHUB_FILE_PATH}`;
    const response = await axios.get(url, {
      headers: { Authorization: `token ${GITHUB_TOKEN}` }
    });
    const fileContent = Buffer.from(response.data.content, 'base64').toString();
    return JSON.parse(fileContent);
  } catch (error) {
    console.error('Failed to load links from GitHub:', error.message);
    return {};
  }
}

async function saveLinksToGitHub(links) {
  try {
    const url = `https://api.github.com/repos/${GITHUB_REPO}/contents/${GITHUB_FILE_PATH}`;
    const fileInfo = await axios.get(url, {
      headers: { Authorization: `token ${GITHUB_TOKEN}` }
    });
    const sha = fileInfo.data.sha;

    await axios.put(url, {
      message: 'Update links.json with new link',
      content: Buffer.from(JSON.stringify(links)).toString('base64'),
      sha: sha
    }, {
      headers: { Authorization: `token ${GITHUB_TOKEN}` }
    });
    console.log('Successfully updated links.json on GitHub.');
  } catch (error) {
    console.error('Failed to update links.json on GitHub:', error.message);
  }
}

async function loadLinks() {
  links = await loadLinksFromGitHub();
  if (Object.keys(links).length === 0) {
    try {
      const data = await fs.readFile(JSON_FILE, 'utf8');
      links = JSON.parse(data);
    } catch (error) {
      links = {};
    }
  }
}

async function saveLinks(links) {
  await fs.writeFile(JSON_FILE, JSON.stringify(links, null, 4));
  await saveLinksToGitHub(links);
}

bot.onText(/\/start/, async (msg) => {
  await bot.sendMessage(msg.chat.id, 
    'Hello! Send me a website name (in lowercase, without spaces), and I\'ll provide the link. ' +
    'If the link doesn\'t exist, you can add it using /add.'
  );
});

bot.onText(/\/add/, async (msg) => {
  userStates[msg.chat.id] = { state: STATES.ENTER_NAME };
  await bot.sendMessage(msg.chat.id, 'Please enter the name of the website you want to add:');
});

bot.onText(/\/cancel/, async (msg) => {
  delete userStates[msg.chat.id];
  await bot.sendMessage(msg.chat.id, 'Link addition canceled.');
});

bot.on('message', async (msg) => {
  if (msg.text.startsWith('/')) return;

  const chatId = msg.chat.id;
  const userState = userStates[chatId];

  if (userState) {
    if (userState.state === STATES.ENTER_NAME) {
      userState.websiteName = msg.text.toLowerCase();
      userState.state = STATES.ENTER_LINK;
      await bot.sendMessage(chatId, 'Now enter the URL of the website:');
    } else if (userState.state === STATES.ENTER_LINK) {
      links[userState.websiteName] = msg.text;
      await saveLinks(links);
      await bot.sendMessage(chatId, `Website '${userState.websiteName}' has been added with the link: ${msg.text}`);
      delete userStates[chatId];
    }
  } else {
    const response = links[msg.text.toLowerCase()] || 'Sorry, I don\'t have a link for that website. Use /add to add it.';
    await bot.sendMessage(chatId, response);
  }
});

app.get('/', async (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/api/links', async (req, res) => {
  res.json(links);
});

app.post(`/${TELEGRAM_BOT_TOKEN}`, async (req, res) => {
  bot.processUpdate(req.body);
  res.send('OK');
});

async function main() {
  await loadLinks();
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
}

main();
