
#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "ReceiveData_TCP.generated.h"

#include "Sockets.h"
#include "SocketSubsystem.h"
#include "Networking.h"

// This class does not need to be modified.
UINTERFACE(MinimalAPI)
class UReceiveData_TCP : public UInterface
{
	GENERATED_BODY()
};

/**
 * 
 */
class FACES_API IReceiveData_TCP
{
	GENERATED_BODY()

	// Add interface functions to this class. This is the class that will be inherited to implement this interface.
public:
};
