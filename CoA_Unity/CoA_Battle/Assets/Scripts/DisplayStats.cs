// Displays stats for players

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class DisplayStats : MonoBehaviour {
	Text stats;

	// Use this for initialization
	void Start () {
		stats = GetComponent<Text> ();
		stats.text = "";
	}

	// Update is called once per frame
	void Update () {
		
	}

	// Add health (from healing)
	void setMessage(int health) {
		stats.text = health.ToString ();
	}
}
