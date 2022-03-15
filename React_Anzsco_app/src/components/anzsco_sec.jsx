import React, { Component, useEffect, useState } from 'react';
import { useLocation,useParams } from "react-router-dom"




const AnzscoSec = () => {

    const location = useLocation();
    const { from } = location.state

    const [isLoaded ,setIsLoaded] = useState(false);

    const [item , setItems] = useState();
    
    
    var stringToHTML = function (str) {
        var dom = document.createElement('div');
        dom.innerHTML = str;
        return dom;
    };
    

        
    useEffect(() =>
    {

        const html = stringToHTML(from);
        const heading = html.textContent.split(/\r?\n/)[0];
        const urlID = stringToHTML(heading);

        const identifier = urlID.textContent.split(" ")[0];


        console.log('http://127.0.0.1:5000/anzsco_sec?heading=' + identifier);


        fetch('http://127.0.0.1:5000/anzsco_sec?heading=' + identifier)
        .then(res => res.json())
        .then(json => {
            setItems(...json);
            setIsLoaded(true);
        });

    },[isLoaded])

    if(isLoaded )
    {   

        const { id, head1, description,
                    skill_level,alternative_titles ,specialisations,
                    skills_assess_authority,caveats,asco_occupations,
                    head2,more_description,tasks,skill_level_desc,occupations_in_this_group} = item;

        
        const occupation  = occupations_in_this_group.slice(1,-1);

        return(     
            <div>
                <div>
                <h1 id='top'>Acacia Imigration Australia</h1>
                </div>
                <div id='secPage'>
                    <h1>{head1}</h1>
                    <dl>
                        <dt>Description</dt>
                        <dd>{description}</dd>

                        <dt>Skill Level</dt>
                        <dd>{skill_level}</dd>

                        <dt>Alternative Titles</dt>
                        <dd dangerouslySetInnerHTML={{__html: alternative_titles}}/>

                        <dt>Specializations</dt>
                        <dd dangerouslySetInnerHTML={{__html: specialisations}} />

                        <dt>Skill Assessment Autority</dt>
                        <dd dangerouslySetInnerHTML={{__html: skills_assess_authority}} />

                        <dt>Caveats</dt>
                        <dd dangerouslySetInnerHTML={{__html: caveats}} />

                        <dt>Asco Occuparions</dt>
                        <dd dangerouslySetInnerHTML={{__html: asco_occupations}} />
                    </dl>
                    <h2>{head2}</h2>
                    <dl>
                        <dt>Description</dt>
                        <dd>{more_description}</dd>


                        <dt>Tasks</dt>
                        <dd dangerouslySetInnerHTML={{__html: tasks}} />


                        <dt>Skill Level</dt>
                        <dd>{skill_level_desc}</dd>
                    </dl>
                    <dl>
                        <dt>Occupations in this Group</dt>
                        <dd dangerouslySetInnerHTML={{__html: occupation}} />
                    </dl>
                    
                    
                </div>
            </div>

        ) 


    }
    else{
        return (

            <div>
                <h1>Loading...</h1>
            </div>
        )
    }
    
    

}
export default AnzscoSec;
    


