const playwright = require('playwright');
const fileSystem = require('fs');
const nodemailer = require("nodemailer");   

let readJsonFile = (fileName) => {
    return fileSystem.readFileSync(fileName,'utf8');
}

let isEqual = (obj1,obj2) => {
    if (obj1.uogQuery != obj2.uogQuery) {
        return false;
    }
    if (obj1.uogSearch != obj2.uogSearch) {
        return false;
    }
    if (obj1.mcgQuery != obj2.mcgQuery) {
        return false;
    }
    if (obj1.mcgSearch != obj2.mcgSearch) {
        return false;
    }
    return true;
}

let whereError = (obj1,obj2) => {
    if (obj1.uogQuery != obj2.uogQuery) {
        return "There was a problem with UoG Query";
    }
    if (obj1.uogSearch != obj2.uogSearch) {
        return "There was a problem with UoG Search";
    }
    if (obj1.mcgQuery != obj2.mcgQuery) {
        return "There was a problem with McGill Query";
    }
    if (obj1.mcgSearch != obj2.mcgSearch) {
        return "There was a problem with McGill Search";
    }
    return "No problem"
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

    let tester = readJsonFile('/home/sysadmin/sprint-1/scraper/json/tester.json');
    tester = JSON.parse(tester);

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

    // ---------------------
    await context.close();
    await browser.close();

    if (isEqual(testObj,tester) == false) { 
		let tmpMessage = "An error has been detected \n" + whereError(testObj,tester) + " ";

        // create reusable transporter object using the default SMTP transport
        const transporter = nodemailer.createTransport({
    		service: 'outlook',
    		auth: {
        		user: 'team6_3760@outlook.com'
                pass: '3760Team6'
    		}
		});
        // send mail with defined transport object
        let info = await transporter.sendMail({
            from: '"Team6 Tester" <team6_3760@outlook.com>', // sender address
            to: "lvelez@uoguelph.ca, htopiwal@uoguelph.ca, jainil@uoguelph.ca, fhamid@uoguelph.ca, nbaker05@uoguelph.ca", // list of receivers
            subject: "There is a problem", // Subject line
            text: tmpMessage, // plain text body
            html: "<b>"+ tmpMessage +"</b>", // html body
        });
    }
}

main();

