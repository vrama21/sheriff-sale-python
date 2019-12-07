Sheriff Sale:

    - [ ] Consider grabbing the address data from the google maps urls provided from the sheriff sale website. This is a more accurate representation of the address and city of the listing.
  
    City Names:
        - [ ] Clean up Buena Names
    Edge Cases:
        - [ ] 1392 Mays Landing Somers Point Rd: 1078 Mays Landing Rd, Somers Point
        - [ ] 1078 Mays Landing Somers Rd: 1078 Mays Landing Rd, Somers Point
        - [ ] 60 Fox Hollow: 60 Fox Hollow Dr
        - [ ] 263 Twenty Second Ave: 263 22nd Ave
        - [ ] 1573 Somers Point Mays Landing Rd: 1573 Somers Point Rd, Egg Harbor Township
        - [ ] 100 S N Carolina Ave: 100 S North Carolina Ave
        - [ ] 13 E Dr: 13 East Dr

Web App:

    Database:
        - [x] Add all NJ counties to Update Database
        - [ ] Build a progress bar to show the progress of the database update
            - 100 / Total Results = % of each row Added
                - (E.g) 400 Results: Each row = 0.25% of width per row added to database
        - [ ] Check for updates and append any new listings

    Table Data:
        - [x] Filter by County, City, & Sale Date
        - [x] Change grid to bootstrap classes
        - [ ] Add secondary filter options (e.g defendant, status history)
            - [x] Dynamically adjust columns to account any adding or removing filters
        - [ ] Sort by Address alphabetically by default
            - [ ] Sort by header (Sale Date, City, or Judgment)
        - [ ] Link images from trulia/zillow
            - [ ] Use a modal to display the images
        - [x] Apply background color to every other row
        - [x] Dynamically make the grid row total = results
        - [ ] Breadcrumbs at the top to show what filters you have selected
        - [ ] Change city form to display cities for only selected county. If county == All, display all.

    HTML:
        - [ ] Consider breaking down the html files into smaller html files (e.g Database Functions, Search Menu) and use the Jinja include methods for cleaner files

    CSS:
        - [x] Restructure all styles in a standard format

Trulia:

    - Build a Trulia Scraper
        - [ ] Data to Gather:
            - [ ] Images
            - [ ] Trulia Estimate
            - [ ] Sq Footage