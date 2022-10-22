import React, {Component} from 'react'
import PostData from './data/records.json'

class Postist extends Component {
  render() {
    return (
       <div className = "App">
        <h1> Student Records</h1>  {
        PostData.map((PostDeail,index)=>( 
        <ol key = { PostDeail.NETID} >
        NetID: {PostDeail.NETID} <br/>
        Name: { PostDeail.Name } <br/>
        Email: { PostDeail.Email } <br/>
        Course#1: { PostDeail['Course#1'] } <br/>
        Course#2: { PostDeail['Course#2'] } <br/>
        Course#3: { PostDeail['Course#3'] } <br/>
        Course#4: { PostDeail['Course#4']} <br/>
        Course#5: { PostDeail['Course#5']} <br/>
        Course#6: { PostDeail['Course#6']} <br/>
        <br/>

        </ol>
    ))
}
</div>
    );
  }
}

export default Postist;
