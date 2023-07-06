terraform {
  backend "s3" {
    bucket = "terraform-state-flaskbb-jpb"
    key    = "core/terraform.tfstate"
    region = "us-west-1"
  }
}
