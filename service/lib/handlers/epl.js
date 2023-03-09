import got from 'got';
import { badRequest, good, internalServerError } from './../shared/responses.js';

const serviceUrl = 'https://v3.football.api-sports.io/teams/statistics',
      rapidApiKey = '421ff937fbc4713a4bef192d62236855'

export default async event => {
  let out = badRequest;
  const { season, team, league } = event.queryStringParameters;
  if( season, team, league ) {
    try {
      const results = await got(serviceUrl, {
        headers: { 'x-rapidapi-key': rapidApiKey },
        searchParams: { season, team, league }
      }).json()
      const {
        response: {
          team: {
            name
          },
          form,
          fixtures: {
            wins: {
              total: totalWins
            },
            loses: {
              total: totalLoses
            },
            draws: {
              total: totalDraws
            }
          },
          goals: {
            for: {
              total: {
                total: totalGoalsFor
              }
            },
            against: {
              total: {
                total: totalGoalsAgainst
              }
            }
          }
        }
      } = results;
      out = good({ name, form, totalWins, totalLoses, totalDraws, totalGoalsFor, totalGoalsAgainst })
    } catch (error) {
      out = internalServerError;
    }
  }
  return out;
};


// headers = {"x-rapidapi-key": secrets['rapidapi_key']}
//         data = network.fetch('https://v3.football.api-sports.io/teams/statistics?season=' + str(self.season) + '&team=' + str(self.team) + '&league=' + str(self.league), headers=headers).json()