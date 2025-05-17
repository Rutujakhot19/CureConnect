from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers
from pyhanko.sign import fields
import io
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from pyhanko.sign import algorithms  # Import the algorithms module


def sign_pdf(input_pdf_path, output_pdf_path, private_key_path, certificate_path):
    """Signs a PDF file using a digital certificate.

    Args:
        input_pdf_path (str): Path to the input PDF file.
        output_pdf_path (str): Path to the output PDF file.
        private_key_path (str): Path to the private key file (PEM format).
        certificate_path (str): Path to the certificate file (PEM format).
    """

    # 1. Load the signing credentials (private key and certificate)
    with open(private_key_path, "rb") as f:
        private_key = load_pem_private_key(f.read(), password=None)  # Replace None with your password if needed
    with open(certificate_path, "rb") as f:
        certificate = load_pem_x509_certificate(f.read())

    signer = signers.SimpleSigner(
        private_key=private_key,
        certificate=certificate,
        # Set the preferred signature mechanism.
        signature_mechanism=algorithms.SignatureMechanism.RSA_PSS,  # Use the enum from the algorithms module
        # Enable long term validation (LTV) where possible.
        embed_validation_info=True,
    )

    # 2. Prepare the PDF document for signing (incremental update)
    with open(input_pdf_path, "rb") as input_pdf:
        pdf_reader = io.BytesIO(input_pdf.read())
        writer = IncrementalPdfFileWriter(pdf_reader)

    # 3. Add a signature field (if one doesn't exist)
    #    This creates an empty signature field that the signature will occupy.
    #    If your PDF already has a signature field, you can skip this.
    fields.append_signature_field(
        writer,
        sig_field_name="Signature1",  # Choose a name for your signature field
        # Optional:  Specify the page and position of the signature field
        box=(10, 10, 150, 50),  # Example:  lower-left x, y, upper-right x, y
        # Optional: Add a text annotation.
        # with fields.SigFieldSpec(on_page=0, box=(10, 10, 150, 50))
    )

    # 4. Sign the PDF
    #    This performs the actual signing operation.
    with open(output_pdf_path, "wb") as output_pdf:
        pdf_signer = signers.PdfSigner(
            signer=signer,
            signature_fields=[
                signers.SigFieldSpec(field_name="Signature1")
            ],  # Reference the name of the signature field
        )
        signed_pdf = pdf_signer.sign_pdf(
            writer,
            output_pdf,
        )
    print(f"Signed PDF saved to {output_pdf_path}")


if __name__ == "__main__":
    # Example usage:
    input_pdf_path = "input.pdf"  # Replace with your input PDF file
    output_pdf_path = "output_signed.pdf"  # Replace with your desired output path
    private_key_path = "private_key.pem"  # Replace with the path to your private key file
    certificate_path = "certificate.pem"  # Replace with the path to your certificate file

    # Generate dummy key and cert for testing.  Replace with your actual keys!
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes
    from cryptography.x509.oid import NameOID
    import datetime

    # Generate RSA key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # Create a self-signed certificate (for testing only - use a real certificate from a CA for production)
    builder = x509.CertificateBuilder().subject_name(
        x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "My Test Certificate")])
    ).issuer_name(
        x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "My Test Certificate")])
    ).not_valid_before(
        datetime.datetime.today() - datetime.timedelta(days=1)
    ).not_valid_after(
        datetime.datetime.today() + datetime.timedelta(days=365)
    ).public_key(public_key).serial_number(
        x509.random_serial_number()
    ).sign(private_key, hashes.SHA256())

    # Save key and cert to files
    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ))
    with open("certificate.pem", "wb") as f:
        f.write(builder.public_bytes(serialization.Encoding.PEM))

    sign_pdf(input_pdf_path, output_pdf_path, private_key_path, certificate_path)