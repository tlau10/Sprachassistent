const axios = require('axios');
const cheerio = require('cheerio');

const regexRemoveSup = new RegExp('\\([0-9a-z,]*\\)', 'g');
const regexRemoveCharacters = new RegExp('[\\|\\(\\\\"),]', 'g');
const regexRemoveSpacing = new RegExp('\\s{2}', 'g');
const regexRemovePriceSpacing = new RegExp('\\s', 'g');
const regexRemoveDay = new RegExp('^\\s[a-zA-Z]*\\.\\s', 'g');

//returns the array of menu jsons 
function getData(html) {
    const dollar = cheerio.load(html);
    return getSpeiseplan(dollar);
}

// loops through all menus on the website and create json for each, adds them into one array
// return: array of JSON-Strings for each menu
function getSpeiseplan(dollar) {
    let allplans = [];

    for (let i = 1; i < 11; i++) {
        const speisePlan = dollar('.contents_' + i + '> .speiseplanTagKat ');
        var output = {};
        output.Date = getDate(dollar, i);
        output.Menu = {};
        speisePlan.each(function () {
            output.Menu[menuTitle(dollar(this))] = {
                "Description": menuDescription(dollar(this)),
                "Price": menuPrice(dollar(this))
            }
        });
        var json = JSON.stringify(output);
        allplans.push(json);
    }
    return allplans;
}

// gets menu title of current menu
// return: menu title
function menuTitle(speisePlan) {
    return speisePlan.find('.category').text();
}

// get the description of current menu
// return: menu description, list of all beilagen 
function menuDescription(speisePlan) {
    let description = speisePlan.find('.title').text();
    //Check if menu description is from beilagen
    if (description.includes("|")) {
        return handleMenuBeilagen(description);
    } else {
        return description.replace(regexRemoveSup, '')
            .replace(regexRemoveCharacters, '')
            .replace(regexRemoveSpacing, ' ');
    }
}


// return: list of all beilagen
function handleMenuBeilagen(beilagen) {
    return beilagen.replace(regexRemoveSup, '')
        .replace(regexRemoveSpacing, '')
        .split("|");
}


// checks if current menu has a price and if so, creates js object of it
// return: js object, eg: { "Studierende" : "5,95€" }
function menuPrice(speisePlan) {
    let p = speisePlan.find('.preise').text();
    let preis = p.replace(regexRemovePriceSpacing, '');
    if (preis !== "") {
        var preisList = preis.replace(regexRemoveSup).split("|");
        var preisObject = {};
        for (let i = 0; i < preisList.length; i++) {
            let preisVariable = preisList[i].split("€");
            preisObject[preisVariable[1]] = preisVariable[0].concat("€");
        }
        return preisObject;
    }
}

// gets date of current menu
// return: date in dd.mm format
function getDate(dollar, i) {
    let date = dollar('.tx-speiseplan > .tabs > .tab' + i).text().replace(regexRemoveDay, '');
    return toStringFromMenuPlanDate(date);
}

// important(!) 
// opens up website and fetches the html data
// async because axios is async, can be used later on when more menu plans are needed
// can later on grab plans simultaneously instead if having to wait for each individual
async function fetchData(url) {
    console.log("Crawling data...");
    // make http call to url
    let response = await axios(url).catch((err) => console.log(err));

    if (response.status !== 200) {
        console.log("Error occurred while fetching data");
        return null;
    }
    return response.data;
}

//functions from dateHelper.js
//
// returns the changed date format from website to day.month
function toStringFromMenuPlanDate(menuDate) {
    let dateArray = menuDate.split('.');
    return padDate(dateArray[0], dateArray[1]);
}

//returns date with an added leading 0, if necessary
function padDate(day, month) {
    return day.padStart(2, '0') + "." + month.padStart(2, '0');
}

module.exports = {
    getData,
    fetchData,
    //for testing purpose only
    getSpeiseplan,
    menuTitle,
    getDate
};