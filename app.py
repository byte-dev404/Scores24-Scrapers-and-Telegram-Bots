# The main centralized file to run both bots on a single server (Designed for fps.ms)

import asyncio
from bot_1 import build_app as build_bot1
from bot_2 import build_app as build_bot2

async def main():
    bot1 = build_bot1()
    bot2 = build_bot2()

    # Proper startup sequence
    await bot1.initialize()
    await bot2.initialize()

    await bot1.start()
    await bot2.start()

    await bot1.bot.initialize()
    await bot2.bot.initialize()

    print("Both bots are running!")

    # Start polling
    await asyncio.gather(
        bot1.updater.start_polling(),
        bot2.updater.start_polling(),
    )

    # Keep process alive forever
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())