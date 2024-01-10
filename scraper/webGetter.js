const playwright = require('playwright');
const fileSystem = require('fs');

let writeJsonFile = (fileName, programArray) => {
    fileSystem.writeFile(fileName, JSON.stringify(programArray, null, '\t'), (err) => {
        if (err) {
            throw err;
        }
    });
}

async function main() {
    // Open a Chromium browser. We use headless: true
    // to run the process in the background.
    const browser = await playwright.chromium.launch({
        headless: true,
        slowMo: 100
    });
    const context = await browser.newContext({ignoreHTTPSErrors: true});
    const page = await context.newPage();

    await page.goto('https://131.104.49.106/');

    let testObj = {
        uogQuery: null,
        mcgQuery: null,
        uogSearch: null,
        mcgSearch: null
    }

    // Select University of Guelph
    await page.selectOption('select', 'University of Guelph');
    // Select Accounting
    await page.selectOption('#ProgramSelector', 'Accounting');
    // Click button:has-text("Search")
    await page.click('button:has-text("Search")');
    testObj.uogQuery = await page.textContent("div#resultTable");
    

    // Select McGill University
    await page.selectOption('select', 'McGill University');
    // Select Bioinformatics
    await page.selectOption('#ProgramSelector', 'Bioinformatics');
    // Click button:has-text("Search")
    await page.click('button:has-text("Search")');
    // Click text=Search
    await page.click('text=Search');
    testObj.mcgQuery = await page.textContent("div#resultTable");

    // assert.equal(page.url(), 'https://131.104.49.106/search');
    // Click [placeholder="Enter\ Course\ code\,\ name"]
    await page.click('text=UoG');
    await page.click('[placeholder="Enter\\ Course\\ code\\,\\ name"]');
    // Fill [placeholder="Enter\ Course\ code\,\ name"]
    await page.fill('[placeholder="Enter\\ Course\\ code\\,\\ name"]', 'CIS');
    // Click button:has-text("Search")
    await page.click('button:has-text("Search")');
    testObj.uogSearch = await page.textContent("div#resultTable");

    // Click text=McGill
    await page.click('text=McGill');
    // Click [placeholder="Enter\ Course\ code\,\ name"]
    await page.click('[placeholder="Enter\\ Course\\ code\\,\\ name"]');
    // Fill [placeholder="Enter\ Course\ code\,\ name"]
    await page.fill('[placeholder="Enter\\ Course\\ code\\,\\ name"]', 'ACCT');
    // Click button:has-text("Search")
    await page.click('button:has-text("Search")');
    testObj.mcgSearch = await page.textContent("div#resultTable");

    writeJsonFile('./json/tester.json',testObj);

    // ---------------------
    await context.close();
    await browser.close();
}

main();

