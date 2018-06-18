###############################################################################
###                            Criação de VM PROMAX                         ###
###############################################################################

#powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Restricted"
#powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Unrestricted"

# VM Name
$VMName          = "promax_cdd" #+ "_" + $env:USERNAME.ToUpper()

#GEOGRAFIAS
$GEOS            = @("ba", "co", "mg", "no", "pr", "rj", "sp", "su")

# Automatic Start Action (Nothing = 0, Start =1, StartifRunning = 2)
$AutoStartAction = 1
# In second
$AutoStartDelay  = 10
# Automatic Start Action (TurnOff = 0, Save =1, Shutdown = 2)
$AutoStopAction  = 1

Write-Host("Nome do servidor: " + $VMName)

###### Hardware Configuration ######
# VM Path
$VMPath         = "C:\vm\promax\" + $VMName

Write-Host("Criando em      : " + $VMPath)

# VM Generation (1 or 2)
$Gen            = 2

# Processor Number
$ProcessorCount = 1

## Memory (Static = 0 or Dynamic = 1)
$MemoryType     = 1

# StaticMemory
$StaticMemory   = 2GB

# DynamicMemory
$StartupMemory  = 2GB
$MinMemory      = 1GB
$MaxMemory      = 4GB

# Sysprep VHD path (The VHD will be copied to the VM folder)
$SysVHDPath     = "\\hb-vw16fseguro\instalador$\vm\promax_01.01.01\promax_rhel_7.vhdx"
# Rename the VHD copied in VM folder to:
$OsDiskName     = $VMName

### Additional virtual drives
$ExtraDrive  = @()
# Drive 1
#$Drive       = New-Object System.Object
#$Drive       | Add-Member -MemberType NoteProperty -Name Name -Value Data
#$Drive       | Add-Member -MemberType NoteProperty -Name Path -Value $($VMPath + "\" + $VMName)
#$Drive       | Add-Member -MemberType NoteProperty -Name Size -Value 10GB
#$Drive       | Add-Member -MemberType NoteProperty -Name Type -Value Dynamic
#$ExtraDrive += $Drive

# Drive 2
#$Drive       = New-Object System.Object
#$Drive       | Add-Member -MemberType NoteProperty -Name Name -Value Bin
#$Drive       | Add-Member -MemberType NoteProperty -Name Path -Value $($VMPath + "\" + $VMName)
#$Drive       | Add-Member -MemberType NoteProperty -Name Size -Value 20GB
#$Drive       | Add-Member -MemberType NoteProperty -Name Type -Value Dynamic
#$ExtraDrive += $Drive
# You can copy/delete this below block as you wish to create (or not) and attach several VHDX

ForEach ($geo in $GEOS) {
    $Drive       = New-Object System.Object
    $Drive       | Add-Member -MemberType NoteProperty -Name Name -Value $("promax_base_" + $geo)
    $Drive       | Add-Member -MemberType NoteProperty -Name Path -Value $VMPath
    $Drive       | Add-Member -MemberType NoteProperty -Name Size -Value 1TB
    $Drive       | Add-Member -MemberType NoteProperty -Name Type -Value Dynamic
    $ExtraDrive += $Drive
    #$log_message = "Disco           : " + "promax_base_" + $geo + ".vhdx"
    #Write-Host($log_message)
}

### Network Adapters
# Primary Network interface: VMSwitch 
$VMSwitchExternal = "vmSwitchExternal"
$VMSwitchInternal = "vmSwitchInternal"
$VlanId       = 0
$VMQ          = $False
$IPSecOffload = $True
$SRIOV        = $False
$MacSpoofing  = $False
$DHCPGuard    = $False
$RouterGuard  = $False
$NicTeaming   = $False

#Search Switch
$VMSwitchExternalExist = $false
$VMSwitchInternalExist = $false
$Switchs = Get-VMSwitch
foreach ($switch in $Switchs) {
    if($switch.Name -eq $VMSwitchExternal) {
        $VMSwitchExternalExist = $true
    }
    if($switch.Name -eq $VMSwitchInternal) {
        $VMSwitchInternalExist = $true
    }
}
# Create Virtual Switch
#$VMSwitch = Get-VMSwitch -Name $VMSwitchExternal
if(!$VMSwitchExternalExist) {
    New-VMSwitch -NetAdapterName "Ethernet" `
                 -Name $VMSwitchExternal `
                 -AllowManagementOS $true

    Write-Host("Switch Virtual  : " + $VMSwitchExternal)
}

if(!$VMSwitchInternalExist) {
    New-VMSwitch -SwitchType Internal `
                 -Name $VMSwitchInternal `

    Write-Host("Switch Virtual  : " + $VMSwitchInternal)
}

## Additional NICs
$NICs  = @()

# NIC 1
$NIC   = New-Object System.Object
$NIC   | Add-Member -MemberType NoteProperty -Name VMSwitch -Value $VMSwitchExternal
$NIC   | Add-Member -MemberType NoteProperty -Name VLAN -Value 10
$NIC   | Add-Member -MemberType NoteProperty -Name VMQ -Value $VMQ
$NIC   | Add-Member -MemberType NoteProperty -Name IPsecOffload -Value $IPSecOffload
$NIC   | Add-Member -MemberType NoteProperty -Name SRIOV -Value $SRIOV
$NIC   | Add-Member -MemberType NoteProperty -Name MacSpoofing -Value $MacSpoofing
$NIC   | Add-Member -MemberType NoteProperty -Name DHCPGuard -Value $DHCPGuard
$NIC   | Add-Member -MemberType NoteProperty -Name RouterGuard -Value $RouterGuard
$NIC   | Add-Member -MemberType NoteProperty -Name NICTeaming -Value $NicTeaming
$NICs += $NIC

Exit
## NIC 2
#$NIC   = New-Object System.Object
#$NIC   | Add-Member -MemberType NoteProperty -Name VMSwitch -Value $VMSwitchExternal
#$NIC   | Add-Member -MemberType NoteProperty -Name VLAN -Value 20
#$NIC   | Add-Member -MemberType NoteProperty -Name VMQ -Value $False
#$NIC   | Add-Member -MemberType NoteProperty -Name IPsecOffload -Value $True
#$NIC   | Add-Member -MemberType NoteProperty -Name SRIOV -Value $False
#$NIC   | Add-Member -MemberType NoteProperty -Name MacSpoofing -Value $False
#$NIC   | Add-Member -MemberType NoteProperty -Name DHCPGuard -Value $False
#$NIC   | Add-Member -MemberType NoteProperty -Name RouterGuard -Value $False
#$NIC   | Add-Member -MemberType NoteProperty -Name NICTeaming -Value $False
#$NICs += $NIC
## You can copy/delete the above block and set it for additional NIC


######################################################
###           VM Creation and Configuration        ###
######################################################

## Creation of the VM
# Creation without VHD and with a default memory value (will be changed after)
New-VM -Name $VMName `
       -Path $VMPath `
       -NoVHD `
       -Generation $Gen `
       -MemoryStartupBytes $MinMemory `
       -SwitchName $VMSwitchExternal

#For booting Linux
Set-VMFirmware $VMName -EnableSecureBoot Off


if ($AutoStartAction -eq 0) {
    $StartAction = "Nothing"
} elseif ($AutoStartAction -eq 1) {
    $StartAction = "Start"
} else {
    $StartAction = "StartIfRunning"
}

if ($AutoStopAction -eq 0) {
    $StopAction = "TurnOff"
} elseif ($AutoStopAction -eq 1) {
    $StopAction = "Save"
} else {
    $StopAction = "Shutdown"
}

## Changing the number of processor and the memory
if (!$MemoryType){
    # If Static Memory    
    Set-VM -Name $VMName `
           -ProcessorCount $ProcessorCount `
           -StaticMemory `
           -MemoryStartupBytes $StaticMemory `
           -AutomaticStartAction $StartAction `
           -AutomaticStartDelay $AutoStartDelay `
           -AutomaticStopAction $StopAction
} else {
    # If Dynamic Memory
    Set-VM -Name $VMName `
           -ProcessorCount $ProcessorCount `
           -DynamicMemory `
           -MemoryMinimumBytes $MinMemory `
           -MemoryStartupBytes $StartupMemory `
           -MemoryMaximumBytes $MaxMemory `
           -AutomaticStartAction $StartAction `
           -AutomaticStartDelay $AutoStartDelay `
           -AutomaticStopAction $StopAction
}

## Set the primary network adapters
$PrimaryNetAdapter = Get-VM $VMName | Get-VMNetworkAdapter
if ($VlanId -gt 0){$PrimaryNetAdapter | Set-VMNetworkAdapterVLAN -Access -VlanId $VlanId}
else{$PrimaryNetAdapter | Set-VMNetworkAdapterVLAN -untagged}

if ($VMQ){$PrimaryNetAdapter | Set-VMNetworkAdapter -VmqWeight 100}
else {$PrimaryNetAdapter | Set-VMNetworkAdapter -VmqWeight 0}

if ($IPSecOffload){$PrimaryNetAdapter | Set-VMNetworkAdapter -IPsecOffloadMaximumSecurityAssociation 512}
else {$PrimaryNetAdapter | Set-VMNetworkAdapter -IPsecOffloadMaximumSecurityAssociation 0}

if ($SRIOV){$PrimaryNetAdapter | Set-VMNetworkAdapter -IovQueuePairsRequested 1 -IovInterruptModeration Default -IovWeight 100}
else{$PrimaryNetAdapter | Set-VMNetworkAdapter -IovWeight 0}

if ($MacSpoofing){$PrimaryNetAdapter | Set-VMNetworkAdapter -MacAddressSpoofing on}
else {$PrimaryNetAdapter | Set-VMNetworkAdapter -MacAddressSpoofing off}

if ($DHCPGuard){$PrimaryNetAdapter | Set-VMNetworkAdapter -DHCPGuard on}
else {$PrimaryNetAdapter | Set-VMNetworkAdapter -DHCPGuard off}

if ($RouterGuard){$PrimaryNetAdapter | Set-VMNetworkAdapter -RouterGuard on}
else {$PrimaryNetAdapter | Set-VMNetworkAdapter -RouterGuard off}

if ($NicTeaming){$PrimaryNetAdapter | Set-VMNetworkAdapter -AllowTeaming on}
else {$PrimaryNetAdapter | Set-VMNetworkAdapter -AllowTeaming off}


## VHD(X) OS disk copy
$log_message = "Copiando VHDX   : " + $SysVHDPath
Write-Host($log_message)
while(!$(Test-Path $SysVHDPath)) {
    Write-Host("Verificando VHDX: Indisponível")
    Start-Sleep -s 1
}
$OsDiskInfo = Get-Item $SysVHDPath
Copy-Item -Path $SysVHDPath -Destination $($VMPath + "\" + $VMName)
Rename-Item -Path $($VMPath + "\" + $VMName + "\" + $OsDiskInfo.Name) -NewName $($OsDiskName + $OsDiskInfo.Extension)
Write-Host("VHDX copiado    : " + $SysVHDPath)

# Attach the VHD(x) to the VM
Add-VMHardDiskDrive -VMName $VMName -Path $($VMPath + "\" + $VMName + "\" + $OsDiskName + $OsDiskInfo.Extension)

$OsVirtualDrive = Get-VMHardDiskDrive -VMName $VMName -ControllerNumber 0
     
# Change the boot order to the VHDX first
Set-VMFirmware -VMName $VMName -FirstBootDevice $OsVirtualDrive

# For additional each Disk in the collection
Foreach ($Disk in $ExtraDrive){
    # if it is dynamic
    if ($Disk.Type -like "Dynamic"){
        New-VHD -Path $($Disk.Path + "\" + $Disk.Name + ".vhdx") `
                -SizeBytes $Disk.Size `
                -Dynamic
        Write-Host("VHDX criado     : " + $Disk.Name + ".vhdx")
    }
    # if it is fixed
    elseif ($Disk.Type -like "Fixed"){
        New-VHD -Path $($Disk.Path + "\" + $Disk.Name + ".vhdx") `
                -SizeBytes $Disk.Size `
                -Fixed
        Write-Host("VHDX criado     : " + $Disk.Name + ".vhdx")
    }

    # Attach the VHD(x) to the Vm
    Add-VMHardDiskDrive -VMName $VMName `
                        -Path $($Disk.Path + "\" + $Disk.Name + ".vhdx")
}

$i = 1
# foreach additional network adapters
Foreach ($NetAdapter in $NICs){
    # add the NIC
    Add-VMNetworkAdapter -VMName $VMName -SwitchName $NetAdapter.VMSwitch -Name "Network Adapter $i"
    
    $ExtraNic = Get-VM -Name $VMName | Get-VMNetworkAdapter -Name "Network Adapter $i" 
    # Configure the NIC regarding the option
    if ($NetAdapter.VLAN -gt 0){$ExtraNic | Set-VMNetworkAdapterVLAN -Access -VlanId $NetAdapter.VLAN}
    else{$ExtraNic | Set-VMNetworkAdapterVLAN -untagged}

    if ($NetAdapter.VMQ){$ExtraNic | Set-VMNetworkAdapter -VmqWeight 100}
    else {$ExtraNic | Set-VMNetworkAdapter -VmqWeight 0}

    if ($NetAdapter.IPSecOffload){$ExtraNic | Set-VMNetworkAdapter -IPsecOffloadMaximumSecurityAssociation 512}
    else {$ExtraNic | Set-VMNetworkAdapter -IPsecOffloadMaximumSecurityAssociation 0}

    if ($NetAdapter.SRIOV){$ExtraNic | Set-VMNetworkAdapter -IovQueuePairsRequested 1 -IovInterruptModeration Default -IovWeight 100}
    else{$ExtraNic | Set-VMNetworkAdapter -IovWeight 0}

    if ($NetAdapter.MacSpoofing){$ExtraNic | Set-VMNetworkAdapter -MacAddressSpoofing on}
    else {$ExtraNic | Set-VMNetworkAdapter -MacAddressSpoofing off}

    if ($NetAdapter.DHCPGuard){$ExtraNic | Set-VMNetworkAdapter -DHCPGuard on}
    else {$ExtraNic | Set-VMNetworkAdapter -DHCPGuard off}

    if ($NetAdapter.RouterGuard){$ExtraNic | Set-VMNetworkAdapter -RouterGuard on}
    else {$ExtraNic | Set-VMNetworkAdapter -RouterGuard off}

    if ($NetAdapter.NicTeaming){$ExtraNic | Set-VMNetworkAdapter -AllowTeaming on}
    else {$ExtraNic | Set-VMNetworkAdapter -AllowTeaming off}

    $log_message = "Placa de Rede   : " + $ExtraNic.Name
    Write-Host($log_message)

    $i++
}

$count = 10
#Inicia a VM
while($count -gt 0) {
    $log_message = $count.ToString() + " segundos para iniciar a VM..."
    Write-Host($log_message)
    Start-Sleep -s 1
    $count--
}
$log_message = "Iniciando a VM..."
Write-Host($log_message)
Start-VM -Name $VMName