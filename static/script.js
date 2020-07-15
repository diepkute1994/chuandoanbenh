function concatstr_id()
{
	var msg='';
	for(i=1; i<8; i++)
	{
		a = document.getElementById('msg'+i).value;
		msg=msg + a + ",";
	}
	msg=msg + document.getElementById('msg8').value;
	document.getElementById("id_value").value = msg+'';
	return msg;
}

function convert_result(d)
{
	if(d=='0')
		return "Không bị tiểu đường";
	return "Bị tiểu đường";
}

function show_result()
{
	concatstr_id();
	var msg_ = document.getElementById("id_value").value;	
	$.get("/get", {p_value : msg_}).done(function(data)
	{
		str_data = data.split(",");
		document.getElementById('idResult').value = convert_result(str_data[0]);
		document.getElementById('idResult_1').value = convert_result(str_data[1]);	
	});
}