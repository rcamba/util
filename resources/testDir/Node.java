class Node
{
	
	private Object data;
	private Node next;
	
	public Node(Object data)
	{
		this.data=data;
		next=null;
		
	}
	
	public Object getData()
	{
		return data;
	}
	
	public Node getNext()
	{
		return next;
	}
	
	
	public void setNext(Node nextNode)
	{
		next=nextNode;
	}
	
	public void setData(Object data)
	{
		this.data=data;
	}
	
	
	public String toString()
	{
		return "Node is holding data: " + data.toString();
	}


}