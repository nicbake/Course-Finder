import React, { Component } from "react";
import { Router, Switch, Route } from "react-router-dom";

import Search from "./search";
import Query from "./query";
import history from "./history";
import ProgramGraph from "./programGraph";
import MajorGraph from "./majorGraph";

export default class Routes extends Component {
    // This will set the extensions to look at the different pages
    render() {
        return (
            <Router history={history}>
                <Switch>
                    <Route path="/" exact component={Query} />
                    <Route path="/query" exact component={Query} />
                    <Route path="/search" exact component={Search} />
                    <Route path="/program" exact component={ProgramGraph} />
                    <Route path="/major" exact component={MajorGraph} />
                </Switch>
            </Router>
        )
    }
}