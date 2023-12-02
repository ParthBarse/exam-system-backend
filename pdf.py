import pdfkit

def html_to_pdf(html_content, output_pdf_path):
    config = pdfkit.configuration(wkhtmltopdf=r"D:\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    pdfkit.from_string(html_content, output_pdf_path, configuration=config)

name = "Parth"

# Example usage
html_content = """
<!DOCTYPE html>
    <title>MCF Admin panel</title>
  </head>
  <body class="font-inter antialiased bg-slate-100 dark:bg-slate-900 text-slate-600 dark:text-slate-400 sidebar-expanded"> 
    <div id="root"><div class="hey"><div class="box"><div class="header"></div><div class="inner-box"><p>Dear<strong> &nbsp; </strong></p></div><div class="table-container"><table class="table"><tr><td>Registration No.</td><td><strong></strong></td><td>Chess No.</td><td><strong></strong></td></tr><tr><td>Name :</td><td colspan="3">undefined undefined</td></tr><tr><td>Camp Name :</td><td></td><td>Batch No :</td><td>ATC23-5</td></tr><tr><td>Total days :</td><td>7 Days</td><td>Camp Category :</td><td> </td></tr><tr><td>Pick Up Point : </td><td></td><td>Pick Up Time :</td><td></td></tr><tr><td>In-chanrge Name :</td><td colspan="3"></td></tr></table></div><div class="in-box-2"><strong>Other Information :- </strong></div><div class="table-container"><table class="table"><tr><td>Camp Place :</td><td><strong></strong></td><td>Camp Date :</td><td><strong>undefined - undefined</strong></td></tr><tr><td>Guardian name :</td><td colspan="3"></td></tr><tr><td>Address :</td><td></td><td>Landmark :</td><td></td></tr><tr><td>Pick Up  :</td><td></td><td>District :</td><td></td></tr><tr><td>State :</td><td></td><td>Pincode :</td><td></td></tr><tr><td>E-mail :</td><td></td><td>contact number :</td><td></td></tr><tr><td>Whatsapp :</td><td></td><td>Fathers number :</td><td></td></tr><tr><td>Blood group :</td><td></td><td>Date of birth :</td><td></td></tr><tr><td>School Name :</td><td colspan="3"></td></tr></table></div><div class="signature"><div class="d-flex"><p>sign</p><p>Camp Commandant</p><p>MCF</p></div></div><div class="terms"><div class="headline"><strong>Terms &amp; Conditions</strong></div><div class="list"><ol><li>Without this Card the Entrance will not be accepted.</li><li>Card will not be accepted if it gets damaged.</li><li>Pick Point given is Fixed, Other than these students will not be picked up.</li><li>Time schedule given is subject to be changed.</li><li>If you have any query regarding Pick up Point or want any other pick up then contact on the below number.</li><li>Bring Medical/Fitness Certificate on the first day of Camp, dated must be before a maximum of 5 Days.</li><li>Without Medical Certificate entry will be prohibited.</li></ol></div></div><div class="footer"><p>Mail us on: <strong>mcfcamp@gmail.com</strong> (mailto:mcfcamp@gmail.com)</p><p>Cantact Us on : 9604082000/9604084000 / Website URL : www.mcfcamp.com (http://mcfcamp.in)</p></div><button class="no-print bg-blue-500 hover:bg-blue-700 text-white py-1 px-8 rounded">Print</button></div></div></div>

</body></html>
"""

output_pdf_path = "output.pdf"

html_to_pdf(html_content, output_pdf_path)
