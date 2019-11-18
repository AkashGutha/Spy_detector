import React, { Component } from 'react'
import spy_data from "./spy_data.json"
import spy_grouped_data from "./spy_grouped_data.json"

export default class Container extends Component {

    componentDidMount() {
        
    }

    constructor(props) {
        super(props)

        console.log(spy_data)
        console.log(spy_grouped_data)
        this.spy_data = JSON.parse(spy_data)
        this.spy_grouped_data = JSON.parse(spy_grouped_data)

        this.state={
            n_spies: 0,
            spie_n_cptured: []
        }

        this.state.n_spies += this.spy_grouped_data.groups.length + this.spy_grouped_data.messy_group.length;
    }

    render() {
        return (
            <div>
                <h1>Spy detector</h1>
                <br />

            </div>
        )
    }
}
