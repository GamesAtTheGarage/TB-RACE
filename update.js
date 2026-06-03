const fs = require("fs");

// TESTDATA (later vervangen door echte Geocaching data)
const tbData = [
    {
        car: "Testcar 2",
        reference: "TB83TQH",
        cache: "GC5GB7R",
        lat: 47.2682,
        lng: 11.3933
    },
    {
        car: "Testcar 3",
        reference: "TBXXXXXX",
        cache: "GC6JQ6X",
        lat: 50.8503,
        lng: 4.3517
    }
];

const output = {
    updated: new Date().toISOString(),
    tb: tbData
};

fs.writeFileSync("locations.json", JSON.stringify(output, null, 2));

console.log("✔ locations.json created/updated");
