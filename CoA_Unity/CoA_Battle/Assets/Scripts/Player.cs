// Player object. Adventurers and enemies inherit from here

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Player : MonoBehaviour {
	bool my_turn; // true if player's turn
	int health;   // basic stats
	int attack;
	int defense;
	int speed;
	Text showStats; // Displays health, attack, etc

	// Use this for initialization
	void Start () {
		my_turn = false;
		showStats = GetComponent<Text> ();
	}

	// Update is called once per frame
	void Update () {
		if (my_turn) { // If player's turn

		}
	}
}


