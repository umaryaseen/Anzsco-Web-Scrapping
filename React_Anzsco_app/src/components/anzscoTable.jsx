import React, { Component } from 'react';
import {  BrowserRouter, Link, Route , Routes } from 'react-router-dom';
import "./anzscoTable.css"
import AnzscoSec from './anzsco_sec';
import { Tooltip } from 'bootstrap';
import $ from 'jquery'

var stringToHTML = function (str) {
    var dom = document.createElement('div');
    dom.innerHTML = str;
    return dom;
};

class AnzscoTable extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            isLoaded : false,
            items : [],
            

        }
    }

    componentDidMount(){

        fetch('http://127.0.0.1:5000/anzsco')
            .then(res => res.json())
            .then(json => {
                this.setState({
                    isLoaded : true,
                    items : json,
                })
            });
    }

    renderTableData() {
        return this.state.items.map((item) => {
            const { id, anzsco_url,authority,
            employer_sponsership,indep_and_family_sponsered ,state_nomination,
            mltssl_stsol,caveat} = item //destructuring
            
            var tooltip = stringToHTML(caveat);
            var tool = 'data-toggle="tooltip"'
            console.log([tooltip.innerHTML.slice(0,5),tool,tooltip.innerHTML.slice(4)].join(''));   
            
            // Select all elements with data-toggle="tooltips" in the document
           // $('[data-toggle="tooltip"]').tooltip();

            return (    

                <tr key={id}>
                    <Link to="/anzsco_sec" state = {{from: anzsco_url }}  >
                    <td dangerouslySetInnerHTML={{__html: anzsco_url}} className= 'list'/></Link>
                    <td>{authority}</td>
                    <td>{employer_sponsership}</td>
                    <td>{indep_and_family_sponsered}</td>
                    <td>{state_nomination}</td>
                    <td>{mltssl_stsol}</td>
                    <td dangerouslySetInnerHTML={{__html: caveat}} />  
                
                </tr>
                
            )
        })
    }

    render() { 
        
        const {isLoaded} = this.state;
        if(isLoaded){
            return (
                

                    <div id = 'main'>
                    <h1 id='title' >ANZSCO Occupations</h1>  
                    <table id='students' className = 'studentTable'>
                        <thead>
                            <th>Anzsco</th>
                            <th>Authority</th>
                            <th>Employer Sponsership</th>
                            <th>Independent and Family Sponsored</th>
                            <th>State Nomination</th>
                            <th>MLTSSL STSOL</th>
                            <th>Caveat</th>
                        </thead>

                        <tbody>
                            
                            {this.renderTableData()}
                            
                        </tbody>
                    </table>
                    </div>
                
            );
        }
        else{   

            return <div>Loading...</div>;
        }
        
    }
}
 
export default AnzscoTable;



