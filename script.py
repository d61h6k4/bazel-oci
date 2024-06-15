from datetime import datetime
import nodriver as uc
import time
import os
import subprocess
from pathlib import Path


async def main():
    time.sleep(5)
    try:
        browser = await uc.start()
    except:
        pass
    browser = await uc.start()
    print("browser is working")
    page = await browser.get("https://www.nowsecure.nl")

    await page.save_screenshot(f"/opt/wd/nowsecure_{datetime.now().isoformat()}")
    await page.get_content()
    await page.scroll_down(150)
    elems = await page.select_all("*[src]")
    for elem in elems:
        await elem.flash()

    page2 = await browser.get("https://twitter.com", new_tab=True)
    page3 = await browser.get(
        "https://github.com/ultrafunkamsterdam/nodriver", new_window=True
    )

    for p in (page, page2, page3):
        await p.bring_to_front()
        await p.scroll_down(200)
        await p  # wait for events to be processed
        await p.reload()
        if p != page3:
            await p.close()
    print("DONE")


if __name__ == "__main__":
    xlock = Path("/tmp/.X0-lock")  # from not cleanly stopping the container
    if xlock.exists():
        xlock.rmdir()
    print("\n### Starting Xvfb...")

    with open(os.devnull, "w") as fnull:
        p = subprocess.Popen(
            ["Xvfb", "-ac", "-screen", "0", "1920x1080x24"],
            stdout=fnull,
            stderr=fnull,
            close_fds=True,
        )

    ret_code = p.poll()
    if ret_code is None:
        print({"message": "xvfb is running"})

    print("\n### Starting fluxbox...")

    with open(os.devnull, "w") as fnull:
        p1 = subprocess.Popen(
            ["fluxbox", "-screen", "0"], stdout=fnull, stderr=fnull, close_fds=True
        )

    ret_code = p1.poll()
    if ret_code is None:
        print({"message": "fluxbox is running"})

    print("\n### Starting ffmpeg...")

    p2 = subprocess.Popen(
        [
            "ffmpeg",
            "-video_size",
            "1720x880",
            "-framerate",
            "25",
            "-f",
            "x11grab",
            "-i",
            ":0.0+100,200",
            "/opt/wd/output.mp4",
        ],
        close_fds=False,
    )

    ret_code = p2.poll()
    if ret_code is None:
        print({"message": "ffmpegis running"})

    # since asyncio.run never worked (for me)
    uc.loop().run_until_complete(main())

    p2.terminate()
    p2.wait(5)
    print("ffmpeg done")
    p1.terminate()
    p.terminate()
