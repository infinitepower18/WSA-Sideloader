# Package Support Framework for MSIX Packaging
The Package Support Framework is used to resolve working directory issues when packaged as an MSIX file. These files need to be included in the MSIX for the program to run, it will crash otherwise if you try to launch it.

Refer to [this document](https://learn.microsoft.com/en-us/windows/msix/psf/psf-current-working-directory#create-and-inject-required-psf-files) for information on including the provided files. The latest version of PSF can be downloaded from [NuGet](https://www.nuget.org/packages/Microsoft.PackageSupportFramework/).
