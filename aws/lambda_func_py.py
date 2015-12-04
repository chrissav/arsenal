console.log('Loading event');
aws = require('aws-sdk');
 
def handler(event, context):
  ecsService = 'flask-app'
  ecsRegion = 'us-east-1'
  maxCount = 2;
 
  ecs = aws.ECS({region: ecsRegion})
  ecs.describeServices({services:[ecsService]}, function(err, data) {
    if err:
      console.log(err, err.stack)
    else:
      desiredCount = data.services[0].desiredCount;
      if desiredCount < maxCount:
        desiredCount+=1;
        var params = {
          service:      ecsService,
          desiredCount: desiredCount
        }
        ecs.updateService(params, function(err, data) {
          if err:
            console.log(err, err.stack)
          else:
            console.log(data)
            context.succeed()
          }
        });
      else:
        console.log('Service count is already max.')
        context.fail()
      }
    }
  });
};