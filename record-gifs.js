// 录制 README 用 GIF:手动驱动 tick 引擎逐帧截图,再用 ImageMagick 合成
// 用法: node record-gifs.js
const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const URL = "file:///mnt/newdisk/github/proxy-evolution/index.html";
const OUT = "/tmp/gif-frames";
const PROJ = "/mnt/newdisk/github/proxy-evolution";
const DELAY = 600;          // 每帧毫秒(≈1.7fps,足够表达包流动且文件小)
const VP = { width: 1280, height: 800 };

(async () => {
  const puppeteer = require("puppeteer-core");
  const browser = await puppeteer.launch({
    headless: "new",
    executablePath: "/usr/bin/google-chrome",
    args: ["--no-sandbox", "--disable-dev-shm-usage", "--hide-scrollbars",
           "--disable-background-timer-throttling", "--disable-renderer-backgrounding",
           "--force-device-scale-factor=1"],
  });

  async function record(name, frames, stepFn, startFn) {
    const dir = path.join(OUT, name);
    fs.rmSync(dir, { recursive: true, force: true });
    fs.mkdirSync(dir, { recursive: true });
    const page = await browser.newPage();
    await page.setViewport(VP);
    await page.goto(URL, { waitUntil: "domcontentloaded" });
    await new Promise(r => setTimeout(r, 900));
    // 重置动画时钟,从干净状态开始
    await page.evaluate(() => { lastT = 0; spawnAcc = 0; burstLeft = 0; nextBurst = 0; });
    if (startFn) await page.evaluate(startFn);
    for (let i = 0; i < frames; i++) {
      await new Promise(r => setTimeout(r, DELAY));
      await page.screenshot({ path: `${dir}/${String(i).padStart(3, "0")}.png` });
      if (stepFn) await page.evaluate(stepFn);
    }
    await page.close();
    const out = `${PROJ}/${name}.gif`;
    execSync(`convert -delay ${DELAY / 10} -loop 0 ${dir}/*.png \
      -resize 75% -layers Optimize -dither FloydSteinberg -colors 128 ${out}`);
    const kb = Math.round(fs.statSync(out).size / 1024);
    console.log(`✓ ${name}.gif  ${frames} 帧  ${kb}KB`);
  }

  // ① 主界面:SS(慢+重传) → 弱网 → 切 QUIC(快+不退让)
  await record("readme-traffic", 42, null, () => {
    document.getElementById("tourClose").click();
    select(0);                       // Shadowsocks
    lastT = 0; spawnAcc = 0; burstLeft = 0;
    setTimeout(() => document.getElementById("netSwitch").click(), 9600);   // 第16帧开弱网
    setTimeout(() => select(3), 19800);                                      // 第33帧切 QUIC
  });

  // ② REALITY 探测剧场:探测包 → 真实网站节点亮起 → 返回真实证书
  await record("readme-probe", 20, null, () => {
    document.getElementById("tourClose").click();
    select(4); theaterSeen = true;   // REALITY,不自动演示,手动触发
    lastT = 0; spawnAcc = 0; burstLeft = 0;
    setTimeout(() => { probing = true; animateProbe(GENS[4]); }, 2400);      // 第4帧发射探测
  });

  // ③ 六代连测:六种判定依次串成演进线
  await record("readme-sweep", 50, null, () => {
    document.getElementById("tourClose").click();
    lastT = 0; spawnAcc = 0; burstLeft = 0;
    setTimeout(() => runChain(), 1800);
  });

  await browser.close();
})();
