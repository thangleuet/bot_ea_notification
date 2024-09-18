# Setting up a Python Script as a Windows Service

## Environment Setup

1. Create a virtual environment and activate it:
    ```bash
    python -m venv env
    env\Scripts\activate
    ```

2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Update Configurations

- Modify the `config.ini` file to set the correct path for the log file:
    ```ini
    data_path = [path_to_log_file]
    ```

## Setting up the Python Script as a Windows Service

1. Download [nssm (Non-Sucking Service Manager)](https://nssm.cc/download) and place the executable in your project folder or add it to your system path.

2. Open **Command Prompt** as Administrator and navigate to your project folder.

3. Install the Python script as a Windows service:
    ```bash
    nssm.exe install bot_ea_service

    Set Path  ---->  {Pathdir}\env\Scripts\python.exe
    Set Starup directory  ----> {Pathdir}\env\Scripts
    Set arguments ---> {Pathdir}\main.py
    ```

4. Specify the Python executable path and your script's location during the service setup.

5. Use the following commands to manage the service:

    - Start the service:
        ```bash
        nssm.exe start bot_ea_service
        ```

    - Stop the service:
        ```bash
        nssm.exe stop bot_ea_service
        ```

    - Remove the service:
        ```bash
        nssm.exe remove bot_ea_service
        ```

