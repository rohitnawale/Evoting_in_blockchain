pragma solidity ^0.4.21;

contract Election_1_2{

    struct Voter{
     // Attributes of Voter
    uint voterID;
    string voterDetailsHashed;
    string voteCastedDetailsHash;
    }
    
    // mapping for indexing voters
    mapping (uint => uint) index;
    
    //A dynamic array for storing voters
    Voter[] public voters;
    
    // A variable to keep count of all the voters
    uint public votersCount;
    
    // Add new voters to the blockchain
    function addVoter(uint _voterID, string _voterDetails)public  {
       
       votersCount++;
       voters.length++;
       voters[voters.length-1].voterID = _voterID;
       voters[voters.length-1].voterDetailsHashed = _voterDetails;
       //voters[voters.length-1].voteCastedDetailsHash = '';
       index[_voterID] = voters.length-1;

   }
   
   // A function to return the details of given voterID
   function getVoter(uint _voterID) public constant returns(uint, string, string){
            return (voters[index[_voterID]].voterID, voters[index[_voterID]].voterDetailsHashed, voters[index[_voterID]].voteCastedDetailsHash);
        }
      
    
    // A function which will return total number of voters   
    function getVoterCount()public constant returns(uint){
        return votersCount;
    }
    
    
    // function to update details of casted vote
    function addCastedDetailsHash(uint _voterID, string memory _details) public{
        voters[index[_voterID]].voteCastedDetailsHash = _details;
    }
       
}

