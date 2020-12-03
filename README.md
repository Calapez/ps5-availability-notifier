# PS5 Availability Notifier

PS5 Availability Notifier is an application that notifies you when the PS5 console is available in two famous portuguese stores: Worten and Fnac.
The notification consists in a loud beep and an e-mail that is sent to any desired account.

This application simply requires you to have the PS5 product page open in the the mentioned stores, it will analyze the elements on the screen to detect when the product is available.

## Installation
Make sure Python 3.x is installed.

```bash
pip install pyscreenshot
```

## Usage
When the program runs, it will save an image of your screen. Use it to find the pixels coordinates that will change when the PS5 becomes available, so that you will get notified.

To run the program use the following command.
```bash
py Main.py
```