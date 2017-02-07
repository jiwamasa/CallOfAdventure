using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Move : MonoBehaviour {

	// Use this for initialization
	void Start () {

	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown (KeyCode.LeftArrow)) {
			transform.Translate(Vector2.left);
		}
		if (Input.GetKeyDown (KeyCode.RightArrow)) {
			transform.Translate(Vector2.right);
		}
	}
}
