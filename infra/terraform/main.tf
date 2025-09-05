locals { 
  bucket = "${var.project}-featback" 
}

resource "aws_s3_bucket" "data" { 
  bucket = local.bucket 
}

resource "aws_iam_role" "redshift_copy_role" {
  name = "${var.project}-redshift-copy"
  assume_role_policy = jsonencode({
    Version="2012-10-17",
    Statement=[{
      Action="sts:AssumeRole",
      Effect="Allow",
      Principal={Service="redshift.amazonaws.com"}
    }]
  })
}

resource "aws_iam_policy" "s3_read" {
  name = "${var.project}-s3-read"
  policy = jsonencode({
    Version="2012-10-17",
    Statement=[{
      Action=["s3:GetObject","s3:ListBucket"],
      Effect="Allow",
      Resource=[aws_s3_bucket.data.arn,"${aws_s3_bucket.data.arn}/*"]
    }]
  })
}

resource "aws_iam_role_policy_attachment" "attach" {
  role = aws_iam_role.redshift_copy_role.name
  policy_arn = aws_iam_policy.s3_read.arn
}
