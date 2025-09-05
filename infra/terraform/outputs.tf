output "s3_bucket" { 
  value = aws_s3_bucket.data.bucket 
}

output "iam_role_arn" { 
  value = aws_iam_role.redshift_copy_role.arn 
}
