# Lonely Discord Music Bot
This bot is a simple music player for Discord voice channels that automatically plays music when someone joins the specified voice channel and stops playing when everyone leaves the channel. Additionally, the bot sends messages to a designated text channel to notify users when someone joins or leaves the channel.


## Setup

1. Clone the repository and `cd` into the directory.

2. Install the required packages using `pip install -r requirements.txt`.

3. Edit the `TOKEN`, `MUSIC_DIR`, `VC_NAME`, and `TXT_CHANNEL_ID` variables in the `lonely_bot.py` file to fit your needs.

4. Run the bot using `python bot.py`.

## Usage

When someone joins the voice channel with the specified name, the bot will join the channel and start playing music from the specified directory until everyone else leaves. When the bot is alone for more than one second, it will leave the voice channel and send a message to the specified text channel.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
