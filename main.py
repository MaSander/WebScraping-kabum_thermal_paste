from analyzing_thermal_paste import analyzing_thermal_paste
from scraping_kabum_thermal_paste import scraping_kabum_thermal_paste
import asyncio

async def main():
    try:
        df = await scraping_kabum_thermal_paste()
        analyzing_thermal_paste(df)
    except Exception as err:
        print(err)

asyncio.run(main())
