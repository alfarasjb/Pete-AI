# Pete-AI
## Pete-AI is a customer service agent for PioneerDev.AI 
### [Conversation Demo](https://youtu.be/WTD1-7IpihA) 
### [Setting a meeting](https://youtu.be/hq8nHJDhBL8)

### Setting up LLM Server

#### Install pyenv

To manage different Python versions, we use `pyenv`. Follow the installation steps based on your operating system:

- **On macOS:**
  ```bash
  brew update
  brew install pyenv
  ```
- **On Ubuntu:**
  ```bash
  sudo apt update
  sudo apt install -y build-essential curl libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
  curl https://pyenv.run | bash
  ```
- **On Windows:**
  - Install pyenv-win via pip:
    ```bash
    pip install pyenv-win --target %USERPROFILE%\\.pyenv
    ```
  - Alternatively, use the manual installation method:
    ```bash
    git clone https://github.com/pyenv-win/pyenv-win.git "$HOME/.pyenv"
    ```

#### Configure your shell environment

Add pyenv to your shell by updating your profile:

- **For macOS and Linux:**
  ```bash
  echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bash_profile
  echo 'eval "$(pyenv init --path)"' >> ~/.bash_profile
  ```
- **For Windows:**
  - Add `%USERPROFILE%\.pyenv\pyenv-win\bin` and `%USERPROFILE%\.pyenv\pyenv-win\shims` to your system's environment variables under 'Path'.

#### Set Up a Virtual Environment

To isolate our project dependencies, we'll set up a virtual environment using `pyenv` and `pyenv-virtualenv`. Follow these steps:

- **Create a virtual environment:**

  ```bash
  pyenv virtualenv venv
  ```

- **Activate the virtual environment:**
  ```bash
  pyenv activate venv
  ```

#### Install Dependencies

With your virtual environment activated, install the required Python packages using `pip`:

- **Install packages:**
  ```bash
  pip install -r requirements.txt
  ```
#### Create an AI Agent 
- Go to your RetellAI [Dashboard](https://beta.retellai.com/dashboard) 
- Navigate to **AI Agents**, and click **Add Agent**
  - Select **Connect Your Own Agent**  
  - You can rename the Agent, and choose a voice. 
  - Note down the **Agent ID**. 
    - This needed for the environment variable: `RETELL_AGENT_ID` later. 
    - Agent ID will be specified when using Twilio calls. 
  - Under **Custom LLM URL**, paste the LLM websocket url with `/llm-websocket` appended to the base URL.
    - Using ngrok: `wss://abcd-12-34-56-789.ngrok.io/llm-websocket` (See **Obtain and Set Up ngrok**) 
    - Using fly: `wss://pete-ai.fly.dev/llm-websocket`

#### Settng Up Calendly API 
- Login to your [Calendly](https://calendly.com) account. 
- On the left-hand navigation panel, select `Integration & apps` 
- In the `All integrations` section, select `API and webhooks` 
- Click `Generate New Token` 
- Enter a name for your token
- Click on `Copy Token`. This will be the environment variable: `CALENDLY_API_KEY`

#### Setting Up Google API  
- Create a new project
  - Navigate to your [Google Cloud Console](https://console.cloud.google.com)  
  - On the upper taskbar, next to the Google Cloud icon on the left-hand side, click the dropdown menu. 
  - On the upper right-hand corner, click `New Project`, and create a new project. 
  - Navigate to your project's dashboard by clicking the project name on the home page.
    - You can find this in the section under your name. With the text: `You're working on project <your-project-name>`
- Enable Google Calendar API 
  - On the project dashboard, select `APIs & Services` on the left-hand panel.  
  - On the search bar, search for `Google Calendar`. Select `Google Calendar API` then click `Enable` 
  - Navigate back to your project's dashboard, then select `APIs & Services`, then select `Credentials` 
  - On the upper taskbar, click `CREATE CREDENTIALS` then select `OAuth client ID` 
    - Select `External`, then enter relevant information for your app such as `App Name`, and your `Email`
    - In the `Scopes` tab, select `ADD OR REMOVE SCOPES`, then select the ff scopes:
      - `.../auth/userninfo.email`
      - `.../auth/userinfo.profile`
      - `openid` 
    - In the `Test users` tab, select `ADD USERS`, here you can add email addresses for test users. 
    - Click `Next and Continue` then `Back To Dashboard` 
  - On the left-hand navigation panel, navigate to `Credentials`, then click `CREATE CREDENTIALS` then select `OAuth client ID`. 
    - Select `Desktop app` as application type. 
    - A popup window will appear, confirming OAuth client has been created. In the popup window, click on `DOWNLOAD JSON`
    - Rename this file to `credentials.json`, and move it to the `scripts` folder in your project directory. 
- Generating the Token 
  - Run the file `scripts/create_google_token.py`. This will create a `token.json` file. 
  - You will be redirected to google. Authenticate with your email, then click `Continue`
  - Copy the contents, this will be the value of the environment variable `GOOGLE_TOKEN`

#### Set Up Environment Variables

- Copy the `.env.example` file to create a `.env` file:
  ```bash
  cp .env.example .env
  ```
- Manually edit the `.env` file and add your environment variables:
  - `OPENAI_API_KEY=your-openai-api-key` 
  - `RETELL_API_KEY=your-retell-api-key`
  - `RETELL_AGENT_ID=your-retell-agent-id`
  - `CALENDLY_API_KEY=your-calendly-api-key`
  - `GOOGLE_TOKEN=your-google-token`

#### Obtain and Set Up ngrok

- Download and install ngrok from [ngrok's website](https://ngrok.com/download).
- Start ngrok with the following command to expose port 8080:
  ```bash
  ngrok http 8080
  ```
- Note the https URL that ngrok provides. You will need this URL to configure Slack to send events to your local machine.
- You can set the `--subdomain` argument to pass in a different subdomain if you're using a paid version of Ngrok.

#### Run the Server

- Enter the following command on the terminal to run the server 
  ```bash
  uvicorn main:app --host 0.0.0.0 --port 8080
  ```
#### Testing on the Dashboard 
- Go to your RetellAI Dashboard and select your AI Agent.
  - For testing on the dashboard, we have to specify a voice. 
  - Click the Voice Name under **Agent ID**. 
  - Select **Echo** (Or you may choose any voice)
- Click **Test Audio**. 
- You can now talk to your agent.
![image](https://github.com/user-attachments/assets/fe1285fd-d846-4b13-affb-86753267d82e)
