# Pete-AI
## Pete-AI is a customer service agent for PioneerDev.AI 

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

#### Set Up Environment Variables

- Copy the `.env.example` file to create a `.env` file:
  ```bash
  cp .env.example .env
  ```
- Manually edit the `.env` file and add your environment variables:
  - `OPENAI_API_KEY=your-openai-api-key` 
  - `RETELL_API_KEY=your-retell-api-key`
  - `RETELL_AGENT_ID=your-retell-agent-id`

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
