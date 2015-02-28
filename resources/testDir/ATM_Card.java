class ATM_Card
{
	private int accNumber, pin;
	
	public ATM_Card(int newAccNumber, int initPin)
	{
		accNumber=newAccNumber;
		pin=initPin;
	}

	public int getPin()
	{
		return pin;
	}

	public void changePin(int newPin)
	{
		pin=newPin;
	}
}