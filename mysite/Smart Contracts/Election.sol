pragma solidity ^0.4.21;

contract Election{
    
    struct Candidate{
    //Attributes of a candidate
    uint id;
    string name;
    string partyName;
    string  region;
    uint voteCount;
   }
   
   struct Voter{
       
    // Attributes of Voter
    uint votingID;
    string name;
    uint age;
    string region;
    string reference_string;
    string beta_string;
    string set_string;
       
   }
   
   //mapping(uint => Candidate) public candidates;
   //for candidates voteCount
   //mapping(uint => Voter) public voters;
   Voter[] public voters;
   Candidate[] public candidates;
   
   uint public votersCount;
   uint public candidatesCount;
   
   function addCandidate (string _name, string _partyName, string _region) public returns(uint){
       candidatesCount++;
       candidates.length++;
       candidates[candidates.length-1].id = candidatesCount;
       candidates[candidates.length-1].name = _name;
       candidates[candidates.length-1].partyName = _partyName;
       candidates[candidates.length-1].region = _region;
       candidates[candidates.length-1].voteCount = 0;
       return candidates.length;
       
   }
   
   
   function addVoter(string _name,  uint _age, string _region)public returns(uint) {
       
       votersCount++;
       voters.length++;
       voters[voters.length-1].votingID = votersCount;
       voters[voters.length-1].name = _name;
      // voters[voters.length-1].password = _password;
       voters[voters.length-1].age = _age;
       voters[voters.length-1].region = _region;
       voters[voters.length-1].reference_string = '';
       voters[voters.length-1].beta_string = '';
       voters[voters.length-1].set_string = '';
       return voters.length;
   }
   
   function getVoter(uint _id) public constant returns(uint, string, uint, string, string, string, string){
            return (voters[_id].votingID, voters[_id].name, voters[_id].age, voters[_id].region, voters[_id].reference_string, voters[_id].beta_string, voters[_id].set_string);
        }
        
    function getVoterCount()public constant returns(uint){
        return votersCount;
    }
    
    function getCandidate(uint _id) public constant returns(uint, string, string, string, uint){
        
        return (candidates[_id].id, candidates[_id].name, candidates[_id].partyName, candidates[_id].region, candidates[_id].voteCount);
    }
    
    function getCandidateCount()public constant returns(uint){
        return candidatesCount;
    }
}