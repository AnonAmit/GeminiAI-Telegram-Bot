# Gemini Telegram Bot

A powerful and versatile chatbot built using the Telegram Bot API and Google's Generative AI.

## Features

* Real-time conversational AI using Google's Gemini-Pro and Gemini-1.5-Pro-Latest models
* Image support with the ability to generate responses based on the content of the image
* Customizable safety settings to ensure appropriate and safe responses
* User-friendly interface with support for MarkdownV2 formatting
* Error handling and fallback mechanisms to ensure a smooth user experience

## Getting Started

1. Create a new Telegram bot and obtain your Telegram token.
2. Set up the environment variables `TG_TOKEN` and `GOOGLE_GEMINI_KEY` in your environment.
3. Install the required dependencies using pip:
```bash
   pip install -r requirements.txt
```
4. Run the bot using the following command:4. Run the bot using the following command:
   ```bash
   python main.py ${TG_TOKEN} ${GOOGLE_GEMINI_API}
   ```
5. Start chatting with your bot on Telegram!

## Environment Variables

* `TG_TOKEN`: Your Telegram bot token.
* `GOOGLE_GEMINI_KEY`: Your Google Gemini API key.

## Dependencies

* `google-generativeai`: Google's Generative AI library.
* `pyTelegramBotAPI`: Telegram Bot API library.

## Contributing

We welcome contributions from the community! If you'd like to contribute, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments

* Google for providing the Generative AI library.
* Telegram for providing the Bot API.
* The community for their support and contributions.
