import * as React from 'react';
import { Container, Row, Col, Stack, Button, ButtonGroup, ToggleButton } from 'react-bootstrap'
import Navbar from './navbar'
import CreateCard from './cardgen'

import '../css/mainstyles.css'

const Search = () => {

    // Query Headers
    const queryHeaders = { 'Accept': 'application/json', 'Content-Type': 'application/json' }

    // Radio values, searchValue Contains the school and radioValue contains the text
    const [searchValue, setSearch] = React.useState('');
    const [radioValue, setRadioValue] = React.useState('1');

    // Submit the search | Search Button Functionality
    const searchSubmit = (e) => {
        e.preventDefault()

        // Create query string with method and headers
        // Parameters are school, term
        const queryString = '/api/search/bar?school=' + radioValue.toString()
            + '&term=' + searchValue.toString();
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

    const radios = [
        { name: 'UoG', value: '1' },
        { name: 'McGill', value: '2' },
    ];

    return (
        <div style={{ width: '100%', height: '100vh', 'background-color': '#EEEEEE' }}>
            {Navbar('/search')}
            <Container>
                <Row className="justify-content-md-center">
                    <Col md={{ span: 6 }}>
                        <Stack gap={3}>
                            <h1 className="text-center">Search for a course</h1>
                            <ButtonGroup>
                                {radios.map((radio, idx) => (
                                    <ToggleButton
                                        key={idx}
                                        id={`radio-${idx}`}
                                        type="radio"
                                        variant={idx % 2 ? 'outline-info' : 'outline-info'}
                                        name="radio"
                                        value={radio.value}
                                        checked={radioValue === radio.value}
                                        onChange={(e) => setRadioValue(e.currentTarget.value)}
                                    >
                                        {radio.name}
                                    </ToggleButton>
                                ))}
                            </ButtonGroup>
                            <input className="form-control" type="text" placeholder="Enter Course code, name" onChange={(e) => setSearch(e.target.value)} />
                            <div className="text-center d-grid">
                                <Button variant="info" type="submit" onClick={searchSubmit}>Search</Button>{' '}
                            </div>
                            <Col>
                                <h1>Results</h1>
                                <div className="table-responsive">
                                    <Row xs={1} md={1} id="resultTable">
                                        <p>Search results will appear here</p>
                                    </Row>
                                </div>
                            </Col>
                        </Stack>
                    </Col>
                </Row>
            </Container>
        </div>
    )
}

export default Search