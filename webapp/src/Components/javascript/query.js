import * as React from 'react';
import { Container, Row, Col, Stack, Button } from 'react-bootstrap'
import Navbar from './navbar'
import CreateCard from './cardgen'

const Query = () => {

    // Query Headers
    const queryHeaders = { 'Accept': 'application/json', 'Content-Type': 'application/json' }

    // set states, these will maintain what the current value of the dropdowns are.
    const [University, setUniversity] = React.useState('');
    const [Program, setProgram] = React.useState('');
    const [Credits, setCredits] = React.useState('');
    const [Offering, setOffering] = React.useState('');

    // Submit the search | Search Button Functionality
    const searchSubmit = (e) => {
        e.preventDefault()

        // Create query string with method and headers
        // Parameters are school, program, credit, offering
        const queryString = '/api/search/filtered?school=' + University.toString()
            + '&program=' + Program.toString()
            + '&credit=' + Credits.toString()
            + '&offering=' + Offering.toString();

        const searchRequest = new Request(queryString, {
            method: 'GET',
            headers: queryHeaders,
        });

        // Fetch request
        fetch(searchRequest)
            .then(response => response.json())
            .then(results => {
                // Get results table and empty it
                let table = document.getElementById('resultTable');
                while (table.hasChildNodes()) {
                    table.removeChild(table.firstChild);
                }
                // Insert each search result into the table
                for (const course in results) {
                    let newCard = CreateCard(results[course]['code'] + ' - ' + results[course]['name'], results[course]['description'], 'Prerequisites: ' + results[course]['prerequisites'], 'Credit: ' + results[course]['credit'], 'Offerings: ' + results[course]['semester']);
                    table.append(newCard);
                }
                // If there was no search result, then display that no results were found
                if (!table.hasChildNodes()) {
                    let emptyP = document.createElement('p');
                    let text = document.createTextNode('No Results Found');
                    emptyP.appendChild(text);
                    table.appendChild(emptyP);
                }
            })
    }

    // Depending on university onchange event, populate the programs table
    const changeUniversity = (event) => {
        event.preventDefault();
        // This will set the current value of university to the selected university
        let university = event.target.value;
        let uniCredits = '';
        if (university === 'University of Guelph') {
            university = 'uog';
            uniCredits = uogCredits;
        }
        if (university === 'McGill University') {
            university = 'mcg';
            uniCredits = mcgCredits;
        }

        if (university === University) return;

        setProgram('');
        setCredits('');

        //Set the university
        setUniversity(university);

        //Clear the programs and credits drop down
        let programs = document.getElementById('ProgramSelector')
        for (let i = programs.options.length - 1; i > 0; i--)
            programs.remove(i);

        let credits = document.getElementById('CreditSelector')
        for (let i = credits.options.length - 1; i > 0; i--)
            credits.remove(i);

        if (university === '') return;

        // Create query string with method and headers
        // Parameters are school
        const queryString = '/api/search/university?school=' + university;
        const searchRequest = new Request(queryString, {
            method: 'GET',
            headers: queryHeaders,
        });
        // Fetch request to api/search which deals with using the parameters to use program to search
        fetch(searchRequest)
            .then(response => response.json())
            .then(results => {
                for (const prog in results) {
                    programs.options[programs.options.length] = new Option(results[prog], results[prog]);
                }
            })

        // Populate Credits drop down
        for (let i = 0; i < uniCredits.length; i++)
            credits.options[credits.options.length] = new Option(uniCredits[i], uniCredits[i]);

        // Dynamic change of Credits based on University
    };

    // Schools, credits and offering seasons
    const schools = [
        "University of Guelph",
        "McGill University",
    ];
    const uogCredits = [
        "0.25",
        "0.50",
        "0.75",
        "1.00",
        "1.75",
        "2.00",
        "2.50",
        "2.75",
        "7.50",
    ];
    const mcgCredits = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    ];
    const offerings = [
        "Winter",
        "Summer",
        "Fall",
    ];

    return (
        <div style={{ width: '100%', height: '100vh', 'background-color': '#EEEEEE' }}>
            {Navbar('/query')}
            <Container>
                <Row>
                    <Col xs={6}>
                        <h1>Filters</h1>
                        <Stack gap={2}>
                            <div className="input-group mb-3">
                                <select className="form-select" id="SchoolSelector" title="School" onChange={changeUniversity}>
                                    <option value=''>School</option>
                                    {schools.map((school) => (<option key={school}>{school}</option>))}
                                </select>
                            </div>

                            <div className="input-group mb-3">
                                <select className="form-select" id="ProgramSelector" title="Program" onChange={(e) => setProgram(e.currentTarget.value)}>
                                    <option value=''>Programs</option>
                                </select>
                            </div>

                            <div className="input-group mb-3">
                                <select className="form-select" id="CreditSelector" title="Credit" onChange={(e) => setCredits(e.currentTarget.value)}>
                                    <option value=''>Credits</option>
                                </select>
                            </div>

                            <div className="input-group mb-3">
                                <select className="form-select" id="inputGroupSelect04" title="Offering" onChange={(e) => setOffering(e.currentTarget.value)}>
                                    <option value=''>Offering</option>
                                    {offerings.map((season) => (<option key={season}>{season}</option>))}
                                </select>
                            </div>
                            <Button variant="info" type="submit" onClick={searchSubmit}>Search</Button>{' '}
                        </Stack>
                    </Col>
                    <Col>
                        <h1>Results</h1>
                        <div className="table-responsive">
                            <Row xs={1} md={1} id="resultTable">
                                <p>Search results will appear here</p>
                            </Row>
                        </div>
                    </Col>
                </Row>
            </Container>
        </div>
    )
}

export default Query