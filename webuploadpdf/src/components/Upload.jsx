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
            selectedpages : [],
            filestate : {}
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
        
        //this.props.socket.send("message", file.name ) 
        
        this.removedfile(file)   
    }

        this.removedfile = file => { console.log('removing...', file)
        this.selectPagesEnable()
        }

        this.selectPagesEnable = () => this.setState({selectpages:true})


        this.dropzone = null;
  

        
        this.props.socket.on('event', this.gotMessage)

        this.props.socket.on('message', this.gotMessage)
           
        
      
    }

    gotMessage = (message) => { 
        console.log(message)
        console.log(JSON.parse(message))

        this.setState( { filestate: JSON.parse(message) } )
        if (this.state.filestate.status === "finished") {
            this.state.outputfile = this.getOutputFile()
        }
    }
   
getOutputFile(){
    let patharray = this.state.filestate.output.split('/')
    let filename=patharray[patharray.length-1]
    return '\\\\bkprcsl01\\secondary-backups\\docs\\converted\\' + filename
 

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
                        <p> {this.state.outputfile ? <a href={this.state.outputfile}>{this.state.outputfile}</a> : ""}                   
                      </p>
                      <p> {this.state.filestate.progress ? this.state.filestate.progress : ""}                   
                      </p>
                      <p> {this.state.filestate.status ? this.state.filestate.status : ""}                   
                      </p>

                  
                  </ul>
                </aside>
              </section>
            );
          }
        }
        
    


