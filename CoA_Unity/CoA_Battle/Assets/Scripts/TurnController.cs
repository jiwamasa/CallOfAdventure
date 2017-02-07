// Keeps track of whose turn it is, and signals players to act

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TurnController : MonoBehaviour {
	bool turn_ended;   // true if player sends signal that they ended turn
	int turn;          // Players/enemies numbered by speed
	int total_players; // How many players there are

	Player[] player_list; // List of players in order of speed

	// Use this for initialization
	void Start () {
		turn = -1;	
		turn_ended = true;
		total_players = 2; // GET FROM DATABASE
		player_list = new Player[total_players]; 
		// POPULATE LIST FROM DATABASE
	}
	
	// Update is called once per frame
	void Update () {
		if (turn_ended) { // If someone has just ended their turn
			turn = (turn + 1)%total_players; // Go to next turn

		}
	}
}
