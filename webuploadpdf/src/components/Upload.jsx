import React, { Component } from 'react'
import DropzoneComponent from 'react-dropzone-component';
import axios from 'axios'
import 'react-dropzone-component/styles/filepicker.css'


export default class Upload extends Component {
   
    constructor(props) {
        super(props);

        // For a full list of possible configurations,
        // please consult http://www.dropzonejs.com/#configuration
        this.djsConfig = {
            addRemoveLinks: true,
            acceptedFiles: "image/jpeg,.pdf"
        };

        this.componentConfig = {
            iconFiletypes: ['.jpg', '.pdf'],
            showFiletypeIcon: true,
            postUrl: 'http://uploadpdf.lbr.lu/uploadHandler'
        };

        // If you want to attach multiple callbacks, simply
        // create an array filled with all your callbacks.
        this.callbackArray = [() => console.log('Hi!'), () => console.log('Ho!')];

        // Simple callbacks work too, of course
        this.callback = () => console.log('Hello!');

        this.success = file => { console.log('uploaded', file); 
        this.props.ws.emit("fileuploaded", file.name )    
    }

        this.removedfile = file => console.log('removing...', file);

        this.dropzone = null;
    }

    render() {
        const config = this.componentConfig;
        const djsConfig = this.djsConfig;

        // For a list of all possible events (there are many), see README.md!
        const eventHandlers = {
            init: dz => this.dropzone = dz,
            drop: this.callbackArray,
            addedfile: this.callback,
            success: this.success,
            removedfile: this.removedfile
        }




            return (
              <section>
                <div className="dropzone" >
                  <DropzoneComponent config={config} eventHandlers={eventHandlers} djsConfig={djsConfig}></DropzoneComponent>
         
                </div>
                <aside>
                  <h2><a href="http://portainer.lbr.lu/#/containers/925698c183adbab9533ee57fcd8f08c17e3e82d5999422aa198612ed4aa5501c/logs">Monitoring</a></h2>
                  <ul>
                  
                  </ul>
                </aside>
              </section>
            );
          }
        }
        
    


