import React, { Component } from 'react'
import DropzoneComponent from 'react-dropzone-component';
import axios from 'axios'
import 'react-dropzone-component/styles/filepicker.css'
import TextField from '@material-ui/core/TextField'

export default class Upload extends Component {
   
    constructor(props) {
        super(props);
        this.state = {
            selectpages : false,
            selectedpages : []
        }
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
        this.props.socket.emit("message", file.name )    
    }

        this.removedfile = file => { console.log('removing...', file);
        this.selectPagesEnable()}

        this.selectPagesEnable = () => this.setState({selectpages:true})


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
                
                  <ul>
                      <TextField > </TextField>

                  
                  </ul>
                </aside>
              </section>
            );
          }
        }
        
    


