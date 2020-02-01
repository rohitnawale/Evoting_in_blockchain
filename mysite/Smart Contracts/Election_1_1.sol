pragma solidity ^0.4.21;

contract Election_1_1{
   struct Voter{
       
    // Attributes of Voter
    uint voterID;
    string voterDetailsHashed;
    string voteCastedDetailsHash;
    
       
   }
   
   //mapping(uint => Candidate) public candidates;
   //for candidates voteCount
   mapping (uint => uint) index;
   Voter[] public voters;
  
   
   uint public votersCount;
   
   
   
   function addVoter(uint _voterID, string _voterDetails)public returns(uint) {
       
       votersCount++;
       voters.length++;
       voters[voters.length-1].voterID = _voterID;
       voters[voters.length-1].voterDetailsHashed = _voterDetails;
       voters[voters.length-1].voteCastedDetailsHash = '';

       //return voters.length;
   }
   
   function getVoter(uint _voterID) public constant returns(uint, string, string){
            return (voters[index[_voterID]].voterID, voters[index[_voterID]].voterDetailsHashed, voters[index[_voterID]].voteCastedDetailsHash);
        }
        
    function getVoterCount()public constant returns(uint){
        return votersCount;
    }
    
    function addCastedDetailsHash(uint _voterID, string _details) public returns(uint){
    
        voters[_voterID].voteCastedDetailsHash = _details;
        return 1;
        
    }
    
    
}